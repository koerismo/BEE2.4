"""Handles Aperture Tag modifications in the compiler."""
import math
import os

import srctools
import utils
import vbsp_options
from conditions import (
    meta_cond, make_result,
    remove_ant_toggle,
    PETI_INST_ANGLE, RES_EXHAUSTED
)
from instanceLocs import resolve as resolve_inst, get_special_inst
from srctools import Vec, Property, VMF, Entity, Output

from vbsp import settings, GAME_MODE

LOGGER = utils.getLogger(__name__)

# A mapping of fizzler targetnames to the base instance
tag_fizzlers = {}

# Maps fizzler targetnames to a set of values. This is used to orient
# floor-attached signs.
tag_fizzler_locs = {}
# The value is a tuple of either ('z', x, y, z),
# ('x', x1, x2, y) or ('y', y1, y2, x).


@meta_cond(priority=200, only_once=True)
def ap_tag_modifications(vmf: VMF, inst: Entity):
    """Perform modifications for Aperture Tag.

    * All fizzlers will be combined with a trigger_paint_cleanser
    * Paint is always present in every map!
    * Suppress ATLAS's Portalgun in coop
    * Override the transition ent instance to have the Gel Gun
    * Create subdirectories with the user's steam ID
    """
    if vbsp_options.get(str, 'game_id') != utils.STEAM_IDS['APTAG']:
        return  # Wrong game!

    LOGGER.info('Performing Aperture Tag modifications...')

    has = settings['has_attr']
    # This will enable the PaintInMap property.
    has['Gel'] = True

    # Set as if the player spawned with no pgun
    has['spawn_dual'] = False
    has['spawn_single'] = False
    has['spawn_nogun'] = True

    for fizz in vmf.by_class['trigger_portal_cleanser']:
        p_fizz = fizz.copy()
        p_fizz['classname'] = 'trigger_paint_cleanser'
        vmf.add_ent(p_fizz)

        if p_fizz['targetname'].endswith('_brush'):
            p_fizz['targetname'] = p_fizz['targetname'][:-6] + '-br_fizz'

        del p_fizz['drawinfastreflection']
        del p_fizz['visible']
        del p_fizz['useScanline']

        for side in p_fizz.sides():
            side.mat = 'tools/toolstrigger'
            side.scale = 0.25

    if GAME_MODE == 'COOP':
        vmf.create_ent(
            classname='info_target',
            targetname='supress_blue_portalgun_spawn',
            origin=vbsp_options.get(Vec, 'global_pti_ents_loc'),
            angles='0 0 0'
        )

    transition_ents = get_special_inst('transitionents')
    for inst in vmf.by_class['func_instance']:
        if inst['file'].casefold() not in transition_ents:
            continue
        inst['file'] = 'instances/bee2/transition_ents_tag.vmf'

    # Because of a bug in P2, these folders aren't created automatically.
    # We need a folder with the user's ID in portal2/maps/puzzlemaker.
    try:
        puzz_folders = os.listdir('../aperturetag/puzzles')
    except FileNotFoundError:
        LOGGER.warning("Aperturetag/puzzles/ doesn't exist??")
    else:
        for puzz_folder in puzz_folders:
            new_folder = os.path.abspath(os.path.join(
                '../portal2/maps/puzzlemaker',
                puzz_folder,
            ))
            LOGGER.info('Creating', new_folder)
            os.makedirs(
                new_folder,
                exist_ok=True,
            )


@meta_cond(priority=-110, only_once=False)
def res_find_potential_tag_fizzlers(vmf: VMF, inst: Entity):
    """We need to know which items are 'real' fizzlers.

    This is used for Aperture Tag paint fizzlers.
    """
    if vbsp_options.get(str, 'game_id') != utils.STEAM_IDS['TAG']:
        return RES_EXHAUSTED

    if inst['file'].casefold() not in resolve_inst('<ITEM_BARRIER_HAZARD:0>'):
        return

    # The key list in the dict will be a set of all fizzler items!
    tag_fizzlers[inst['targetname']] = inst

    if tag_fizzler_locs:  # Only loop through fizzlers once.
        return

    # Determine the origins by first finding the bounding box of the brushes,
    # then averaging.
    for fizz in vmf.by_class['trigger_portal_cleanser']:
        name = fizz['targetname'][:-6]  # Strip off '_brush'
        bbox_min, bbox_max = fizz.get_bbox()
        if name in tag_fizzler_locs:
            orig_min, orig_max = tag_fizzler_locs[name]
            orig_min.min(bbox_min)
            orig_max.max(bbox_max)
        else:
            tag_fizzler_locs[name] = bbox_min, bbox_max

    for name, (s, l) in tag_fizzler_locs.items():
        # Figure out how to compare for this brush.
        # If it's horizontal, signs should point to the center:
        if abs(s.z - l.z) == 2:
            tag_fizzler_locs[name] =(
                'z',
                s.x + l.x / 2,
                s.y + l.y / 2,
                s.z + 1,
            )
            continue
        # For the vertical directions, we want to compare based on the line segment.
        if abs(s.x - l.x) == 2:  # Y direction
            tag_fizzler_locs[name] = (
                'y',
                s.y,
                l.y,
                s.x + 1,
            )
        else:  # Extends in X direction
            tag_fizzler_locs[name] = (
                'x',
                s.x,
                l.x,
                s.y + 1,
            )


@make_result('TagFizzler')
def res_make_tag_fizzler(vmf: VMF, inst: Entity, res: Property):
    """Add an Aperture Tag Paint Gun activation fizzler.

    These fizzlers are created via signs, and work very specially.
    MUST be priority -100 so it runs before fizzlers!
    """
    import vbsp
    if vbsp_options.get(str, 'game_id') != utils.STEAM_IDS['TAG']:
        # Abort - TAG fizzlers shouldn't appear in any other game!
        inst.remove()
        return

    fizz_base = fizz_name = None

    # Look for the fizzler instance we want to replace
    for targetname in inst.output_targets():
        if targetname in tag_fizzlers:
            fizz_name = targetname
            fizz_base = tag_fizzlers[targetname]
            del tag_fizzlers[targetname]  # Don't let other signs mod this one!
            continue
        else:
            # It's an indicator toggle, remove it and the antline to clean up.
            LOGGER.warning('Toggle: {}', targetname)
            for ent in vmf.by_target[targetname]:
                remove_ant_toggle(ent)
    inst.outputs.clear()  # Remove the outptuts now, they're not valid anyway.

    if fizz_base is None:
        # No fizzler - remove this sign
        inst.remove()
        return

    # The distance from origin the double signs are seperated by.
    sign_offset = res.int('signoffset', 16)

    sign_loc = (
        # The actual location of the sign - on the wall
        Vec.from_str(inst['origin']) +
        Vec(0, 0, -64).rotate_by_str(inst['angles'])
    )

    # Now deal with the visual aspect:
    # Blue signs should be on top.

    blue_enabled = srctools.conv_bool(inst.fixup['$start_enabled'])
    oran_enabled = srctools.conv_bool(inst.fixup['$start_reversed'])

    if not blue_enabled and not oran_enabled:
        # Hide the sign in this case!
        inst.remove()

    inst_angle = srctools.parse_vec_str(inst['angles'])

    inst_normal = Vec(0, 0, 1).rotate(*inst_angle)
    loc = Vec.from_str(inst['origin'])

    if blue_enabled and oran_enabled:
        inst['file'] = res['frame_double']
        # On a wall, and pointing vertically
        if inst_normal.z != 0 and Vec(0, 1, 0).rotate(*inst_angle).z != 0:
            # They're vertical, make sure blue's on top!
            blue_loc = Vec(loc.x, loc.y, loc.z + sign_offset)
            oran_loc = Vec(loc.x, loc.y, loc.z - sign_offset)
        else:
            offset = Vec(0, sign_offset, 0).rotate(*inst_angle)
            blue_loc = loc + offset
            oran_loc = loc - offset
    else:
        inst['file'] = res['frame_single']
        # They're always centered
        blue_loc = loc
        oran_loc = loc

    if inst_normal.z != 0:
        # If on floors/ceilings, rotate to point at the fizzler!
        sign_floor_loc = sign_loc.copy()
        sign_floor_loc.z = 0  # We don't care about z-positions.

        # Grab the data saved earlier in res_find_potential_tag_fizzlers()
        axis, side_min, side_max, normal = tag_fizzler_locs[fizz_name]

        # The Z-axis fizzler (horizontal) must be treated differently.
        if axis == 'z':
            # For z-axis, just compare to the center point.
            # The values are really x, y, z, not what they're named.
            sign_dir = sign_floor_loc - (side_min, side_max, normal)
        else:
            # For the other two, we compare to the line,
            # or compare to the closest side (in line with the fizz)
            other_axis = 'x' if axis == 'y' else 'y'
            if abs(sign_floor_loc[other_axis] - normal) < 32:
                # Compare to the closest side. Use ** to swap x/y arguments
                # appropriately. The closest side is the one with the
                # smallest magnitude.
                vmf.create_ent(
                    classname='info_null',
                    targetname=inst['targetname'] + '_min',
                    origin=sign_floor_loc - Vec(**{
                        axis: side_min,
                        other_axis: normal,
                    }),
                )
                vmf.create_ent(
                    classname='info_null',
                    targetname=inst['targetname'] + '_max',
                    origin=sign_floor_loc - Vec(**{
                        axis: side_max,
                        other_axis: normal,
                    }),
                )
                sign_dir = min(
                    sign_floor_loc - Vec(**{
                        axis: side_min,
                        other_axis: normal,
                    }),
                    sign_floor_loc - Vec(**{
                        axis: side_max,
                        other_axis: normal,
                    }),
                    key=Vec.mag,
                )
            else:
                # Align just based on whether we're in front or behind.
                sign_dir = Vec()
                sign_dir[other_axis] = sign_floor_loc[other_axis] - normal

        sign_angle = math.degrees(
            math.atan2(sign_dir.y, sign_dir.x)
        )
        # Round to nearest 90 degrees
        # Add 45 so the switchover point is at the diagonals
        sign_angle = (sign_angle + 45) // 90 * 90

        # Rotate to fit the instances - south is down
        sign_angle = int(sign_angle + 90) % 360
        if inst_normal.z > 0:
            sign_angle = '0 {} 0'.format(sign_angle)
        elif inst_normal.z < 0:
            # Flip upside-down for ceilings
            sign_angle = '0 {} 180'.format(sign_angle)
    else:
        # On a wall, face upright
        sign_angle = PETI_INST_ANGLE[inst_normal.as_tuple()]

    if blue_enabled:
        vmf.create_ent(
            classname='func_instance',
            file=res['blue_sign', ''],
            targetname=inst['targetname'],
            angles=sign_angle,
            origin=blue_loc.join(' '),
        )

    if oran_enabled:
        vmf.create_ent(
            classname='func_instance',
            file=res['oran_sign', ''],
            targetname=inst['targetname'],
            angles=sign_angle,
            origin=oran_loc.join(' '),
        )

    # Now modify the fizzler...

    fizz_brushes = list(
        vmf.by_class['trigger_portal_cleanser'] &
        vmf.by_target[fizz_name + '_brush']
    )

    if 'base_inst' in res:
        fizz_base['file'] = resolve_inst(res['base_inst'])[0]
    fizz_base.outputs.clear()  # Remove outputs, otherwise they break
    # branch_toggle entities

    # Subtract the sign from the list of connections, but don't go below
    # zero
    fizz_base.fixup['$connectioncount'] = str(max(
        0,
        srctools.conv_int(fizz_base.fixup['$connectioncount', ''], 0) - 1
    ))

    if 'model_inst' in res:
        model_inst = resolve_inst(res['model_inst'])[0]
        for mdl_inst in vmf.by_class['func_instance']:
            if mdl_inst['targetname', ''].startswith(fizz_name + '_model'):
                mdl_inst['file'] = model_inst

    # Find the direction the fizzler front/back points - z=floor fizz
    # Signs will associate with the given side!
    bbox_min, bbox_max = fizz_brushes[0].get_bbox()
    for axis, val in zip('xyz', bbox_max-bbox_min):
        if val == 2:
            fizz_axis = axis
            sign_center = (bbox_min[axis] + bbox_max[axis]) / 2
            break
    else:
        # A fizzler that's not 128*x*2?
        raise Exception('Invalid fizzler brush ({})!'.format(fizz_name))

    # Figure out what the sides will set values to...
    pos_blue = False
    pos_oran = False
    neg_blue = False
    neg_oran = False
    if sign_loc[fizz_axis] < sign_center:
        pos_blue = blue_enabled
        pos_oran = oran_enabled
    else:
        neg_blue = blue_enabled
        neg_oran = oran_enabled

    fizz_off_tex = {
        'left': res['off_left'],
        'center': res['off_center'],
        'right': res['off_right'],
        'short': res['off_short'],
    }
    fizz_on_tex = {
        'left': res['on_left'],
        'center': res['on_center'],
        'right': res['on_right'],
        'short': res['on_short'],
    }

    # If it activates the paint gun, use different textures
    if pos_blue or pos_oran:
        pos_tex = fizz_on_tex
    else:
        pos_tex = fizz_off_tex

    if neg_blue or neg_oran:
        neg_tex = fizz_on_tex
    else:
        neg_tex = fizz_off_tex

    if vbsp.GAME_MODE == 'COOP':
        # We need ATLAS-specific triggers
        pos_trig = vmf.create_ent(
            classname='trigger_playerteam',
        )
        neg_trig = vmf.create_ent(
            classname='trigger_playerteam',
        )
        output = 'OnStartTouchBluePlayer'
    else:
        pos_trig = vmf.create_ent(
            classname='trigger_multiple',
        )
        neg_trig = vmf.create_ent(
            classname='trigger_multiple',
            spawnflags='1',
        )
        output = 'OnStartTouch'

    pos_trig['origin'] = neg_trig['origin'] = fizz_base['origin']
    pos_trig['spawnflags'] = neg_trig['spawnflags'] = '1'  # Clients Only

    pos_trig['targetname'] = fizz_name + '-trig_pos'
    neg_trig['targetname'] = fizz_name + '-trig_neg'

    pos_trig.outputs = [
        Output(
            output,
            fizz_name + '-trig_neg',
            'Enable',
        ),
        Output(
            output,
            fizz_name + '-trig_pos',
            'Disable',
        ),
    ]

    neg_trig.outputs = [
        Output(
            output,
            fizz_name + '-trig_pos',
            'Enable',
        ),
        Output(
            output,
            fizz_name + '-trig_neg',
            'Disable',
        ),
    ]

    voice_attr = vbsp.settings['has_attr']

    if blue_enabled:
        # If this is blue/oran only, don't affect the other color
        neg_trig.outputs.append(Output(
            output,
            '@BlueIsEnabled',
            'SetValue',
            param=srctools.bool_as_int(neg_blue),
        ))
        pos_trig.outputs.append(Output(
            output,
            '@BlueIsEnabled',
            'SetValue',
            param=srctools.bool_as_int(pos_blue),
        ))
        # Add voice attributes - we have the gun and gel!
        voice_attr['bluegelgun'] = True
        voice_attr['bluegel'] = True
        voice_attr['bouncegun'] = True
        voice_attr['bouncegel'] = True

    if oran_enabled:
        neg_trig.outputs.append(Output(
            output,
            '@OrangeIsEnabled',
            'SetValue',
            param=srctools.bool_as_int(neg_oran),
        ))
        pos_trig.outputs.append(Output(
            output,
            '@OrangeIsEnabled',
            'SetValue',
            param=srctools.bool_as_int(pos_oran),
        ))
        voice_attr['orangegelgun'] = True
        voice_attr['orangegel'] = True
        voice_attr['speedgelgun'] = True
        voice_attr['speedgel'] = True

    if not oran_enabled and not blue_enabled:
        # If both are disabled, we must shutdown the gun when touching
        # either side - use neg_trig for that purpose!
        # We want to get rid of pos_trig to save ents
        vmf.remove_ent(pos_trig)
        neg_trig['targetname'] = fizz_name + '-trig'
        neg_trig.outputs.clear()
        neg_trig.add_out(Output(
            output,
            '@BlueIsEnabled',
            'SetValue',
            param='0'
        ))
        neg_trig.add_out(Output(
            output,
            '@OrangeIsEnabled',
            'SetValue',
            param='0'
        ))

    for fizz_brush in fizz_brushes:  # portal_cleanser ent, not solid!
        # Modify fizzler textures
        bbox_min, bbox_max = fizz_brush.get_bbox()
        for side in fizz_brush.sides():
            norm = side.normal()
            if norm[fizz_axis] == 0:
                # Not the front/back: force nodraw
                # Otherwise the top/bottom will have the odd stripes
                # which won't match the sides
                side.mat = 'tools/toolsnodraw'
                continue
            if norm[fizz_axis] == 1:
                side.mat = pos_tex[
                    vbsp.TEX_FIZZLER[
                        side.mat.casefold()
                    ]
                ]
            else:
                side.mat = neg_tex[
                    vbsp.TEX_FIZZLER[
                        side.mat.casefold()
                    ]
                ]
        # The fizzler shouldn't kill cubes
        fizz_brush['spawnflags'] = '1'

        fizz_brush.outputs.append(Output(
            output,
            '@shake_global',
            'StartShake',
        ))

        fizz_brush.outputs.append(Output(
            output,
            '@shake_global_sound',
            'PlaySound',
        ))

        # The triggers are 8 units thick, 24 from the center
        # (-1 because fizzlers are 2 thick on each side).
        neg_min, neg_max = Vec(bbox_min), Vec(bbox_max)
        neg_min[fizz_axis] -= 23
        neg_max[fizz_axis] -= 17

        pos_min, pos_max = Vec(bbox_min), Vec(bbox_max)
        pos_min[fizz_axis] += 17
        pos_max[fizz_axis] += 23

        if blue_enabled or oran_enabled:
            neg_trig.solids.append(
                vmf.make_prism(
                    neg_min,
                    neg_max,
                    mat='tools/toolstrigger',
                ).solid,
            )
            pos_trig.solids.append(
                vmf.make_prism(
                    pos_min,
                    pos_max,
                    mat='tools/toolstrigger',
                ).solid,
            )
        else:
            # If neither enabled, use one trigger
            neg_trig.solids.append(
                vmf.make_prism(
                    neg_min,
                    pos_max,
                    mat='tools/toolstrigger',
                ).solid,
            )