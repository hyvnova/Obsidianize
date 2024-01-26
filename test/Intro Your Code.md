Bevy Version:0.12(current)


Intro: Your Code
This page is an overview, to give you an idea of the big picture of how Bevy
works. Click on the various links to be taken to dedicated pages where you can
learn more about each concept.

As mentioned in the ECS Intro, Bevy manages all of your
functionality/behaviors for you, running them when appropriate and giving them
access to whatever parts of your data they need.
Individual pieces of functionality are called systems. Each system
is a Rust function (fn) you write, which accepts special parameter
types to indicate what data it needs to
access. Think of the function signature as a "specification" for what to fetch
from the ECS World.
Here is what a system might look like. Note how, just by looking
at the function parameters, we know exactly what data
can be accessed.
fn enemy_detect_player(
    // access data from resources
    mut ai_settings: ResMut<EnemyAiSettings>,
    gamemode: Res<GameModeData>,
    // access data from entities/components
    query_player: Query<&Transform, With<Player>>,
    query_enemies: Query<&mut Transform, (With<Enemy>, Without<Player>)>,
    // in case we want to spawn/despawn entities, etc.
    mut commands: Commands,
) {
    // ... implement your behavior here ...
}
(learn more about: systems, queries, commands, resources, entities, components)
Parallel Systems
Based on the parameter types of the systems
you write, Bevy knows what data each system can access and whether it conflicts
with any other systems.  Systems that do not conflict (don't access any of the
same data mutably) will be automatically run in parallel
on different CPU threads. This way, you get multithreading, utilizing modern
multi-core CPU hardware effectively, with no extra effort from you!
For best parallelism performance, it is recommended that you keep your
functionality and your data granular. Create many small
systems, each one with a narrowly-scoped purpose and accessing only the data it
needs. This gives Bevy more opportunities for parallelism. Putting too much
functionality in one system, or too much data in a single
component or resource struct, limits parallelism.
Bevy's parallelism is non-deterministic by default. Your systems might run in a
different and unpredictable order relative to one another, unless you add
ordering dependencies to constrain it.
Exclusive Systems
Exclusive systems provide you with a way to get full direct
access to the ECS World. They cannot run in parallel
with other systems, because they can access anything and do anything. Sometimes,
you might need this additonal power.
fn save_game(
    // get full access to the World, so we can access all data and do anything
    world: &mut World,
) {
    // ... save game data to disk, or something ...
}
Schedules
Bevy stores systems inside of schedules
(Schedule). The schedule contains the systems and all
relevant metadata to organize them, telling Bevy when and how to run them. Bevy
Apps typically contain many schedules. Each one is a collection of
systems to be invoked in different scenarios (every frame update, fixed
timestep update, at app startup, on state
transitions, etc.).
The metadata stored in schedules allows you to control how systems run:

Add run conditions to control if systems should run during an
invocation of the schedule. You can disable systems if you only need them
to run sometimes.
Add ordering constraints, if one system depends on
another system completing before it.

Within schedules, systems can be grouped into sets. Sets
allow multiple systems to share common configuration/metadata. Systems
inherit configuration from all sets they belong to. Sets can also inherit
configuration from other sets.
Here is an illustration to help you visualize the logical structure of a
schedule. Let's look at how a hypothetical "Update" (run every frame) schedule of a
game might be organized.
List of systems:
System nameSets it belongs toRun conditionsOrdering constraints
footstep_soundAudioSet GameplaySetafter(player_movement) after(enemy_movement)
player_movementGameplaySetplayer_alive not(cutscene)after(InputSet)
camera_movementGameplaySetafter(InputSet)
enemy_movementEnemyAiSet
enemy_spawnEnemyAiSet
enemy_despawnEnemyAiSetbefore(enemy_spawn)
mouse_inputInputSetmouse_enabled
controller_inputInputSetgamepad_enabled
background_musicAudioSet
ui_button_animate
menu_logo_animateMainMenuSet
menu_button_soundMainMenuSet AudioSet
...


List of sets:
Set nameParent SetsRun conditionsOrdering constraints
MainMenuSetin_state(MainMenu)
GameplaySetin_state(InGame)
InputSetGameplaySet
EnemyAiSetGameplaySetnot(cutscene)after(player_movement)
AudioSetnot(audio_muted)


Note that it doesn't matter in what order systems are listed in the schedule.
Their order of execution is determined by the metadata. Bevy
will respect those constraints, but otherwise run systems in parallel as much as
it can, depending on what CPU threads are available.
Also note how our hypothetical game is implemented using many individually-small
systems. For example, instead of playing audio inside of the player_movement
system, we made a separate play_footstep_sounds system. These two pieces of
functionality probably need to access different data, so
putting them in separate systems allows Bevy more opportunities for parallelism.
By being separate systems, they can also have different configuration. The
play_footstep_sounds system can be added to an AudioSet
set, from which it inherits a not(audio_muted) run
condition.
Similarly, we put mouse and controller input in separate systems. The InputSet
set allows systems like player_movement to share an ordering dependency
on all of them at once.
You can see how Bevy's scheduling APIs give you a lot of flexibility to organize
all the functionality in your game. What will you do with all this power? ;)

Here is how schedule that was illustrated above could be
created in code:
// Set configuration is per-schedule. Here we do it for `Update`
app.configure_sets(Update, (
    MainMenuSet
        .run_if(in_state(MainMenu)),
    GameplaySet
        .run_if(in_state(InGame)),
    InputSet
        .in_set(GameplaySet),
    EnemyAiSet
        .in_set(GameplaySet)
        .run_if(not(cutscene))
        .after(player_movement),
    AudioSet
        .run_if(not(audio_muted)),
));
app.add_systems(Update, (
    (
        ui_button_animate,
        menu_logo_animate.in_set(MainMenuSet),
    ),
    (
        enemy_movement,
        enemy_spawn,
        enemy_despawn.before(enemy_spawn),
    ).in_set(EnemyAiSet),
    (
        mouse_input.run_if(mouse_enabled),
        controller_input.run_if(gamepad_enabled),
    ).in_set(InputSet),
    (
        footstep_sound.in_set(GameplaySet),
        menu_button_sound.in_set(MainMenuSet),
        background_music,
    ).in_set(AudioSet),
    (
        player_movement
            .run_if(player_alive)
            .run_if(not(cutscene)),
        camera_movement,
    ).in_set(GameplaySet).after(InputSet),
));
(learn more about: schedules, system sets, states, run conditions, system ordering)

### References
[[The App  Unofficial Bevy Cheat Book]] [[Run Criteria  Unofficial Bevy Cheat Book]] [[Systems  Unofficial Bevy Cheat Book]] [[Direct ECS World Access  Unofficial Bevy Cheat Book]] [[States  Unofficial Bevy Cheat Book]] [[List of Bevy Builtins  Unofficial Bevy Cheat Book]] [[Intro Your Data  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] [[System Sets  Unofficial Bevy Cheat Book]] [[Commands  Unofficial Bevy Cheat Book]] [[Entities Components  Unofficial Bevy Cheat Book]] [[Exclusive Systems  Unofficial Bevy Cheat Book]] [[Intro to ECS  Unofficial Bevy Cheat Book]] [[Entities Components  Unofficial Bevy Cheat Book]] [[Queries  Unofficial Bevy Cheat Book]] [[Schedules  Unofficial Bevy Cheat Book]] [[System Order of Execution  Unofficial Bevy Cheat Book]] [[Fixed Timestep  Unofficial Bevy Cheat Book]] [[Resources  Unofficial Bevy Cheat Book]] 