from pathlib import Path

'''world dimensions and frame rate'''
World_width = 1280
World_height = 720
World_size = (World_width, World_height)
FPS = 60

''' fixed time step used by the trajectory preview '''
Fixed_dt = 1 / 120

Gravity = (0,900)
Ground_top = World_height - 60

''''when pojectile counts as 'at rest'.  '''
Rest_speed = 20
Rest_steps = 48
Max_shot_time = 12

''''  how aiming and launch power feels'''
Drag_radius = 120
Power_scale = 6.5
Max_launch_power = 900
Trajectory_steps = 60

Remaining_projectile_bonus = 50

Bomb_blast_radius = 150
Bomb_blast_damage = 45
Bomb_blast_impulse = 420

'''user data directory for saving settings and progress'''
User_data_dir = Path.home() / ".shivoragames" / "skyhurler"

'''how many physics substeps so fast balls do not tunnel through walls'''
Max_substeps = 4

'''how long a spent ball stays on screen before it fades'''
Spent_projectile_lifetime = 2.5

'''splitter ability'''
Split_spread_degrees = 15.0
Split_child_mass_fraction = 1 / 3
Split_child_radius_fraction = 0.8

'''level 4 boss'''
Boss_max_hp = 300
Boss_weak_point_multiplier = 2.0
Boss_enrage_hp_fraction = 1 / 3

'''impact damage is Impact_damage_scale * mass * impact speed'''
Impact_damage_scale = 0.04

'''collapsing structures'''
Max_cascade_depth = 8
Cascade_falloff = 0.6
Collapse_margin = 24.0
Collapse_enemy_damage = 40.0
