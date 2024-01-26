Bevy Version:0.9(outdated!)


States
Relevant official examples:
state.

States allow you to structure the runtime "flow" of your app.
This is how you can implement things like:

A menu screen or a loading screen
Pausing / unpausing the game
Different game modes
…

In every state, you can have different systems running. You
can also add one-shot setup and cleanup systems to run when entering or
exiting a state.
To use states, define an enum type and add system sets
to your app builder:
#[derive(Debug, Clone, Eq, PartialEq, Hash)]
enum AppState {
    MainMenu,
    InGame,
    Paused,
}

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)

        // add the app state type
        .add_state(AppState::MainMenu)

        // add systems to run regardless of state, as usual
        .add_system(play_music)

        // systems to run only in the main menu
        .add_system_set(
            SystemSet::on_update(AppState::MainMenu)
                .with_system(handle_ui_buttons)
        )

        // setup when entering the state
        .add_system_set(
            SystemSet::on_enter(AppState::MainMenu)
                .with_system(setup_menu)
        )

        // cleanup when exiting the state
        .add_system_set(
            SystemSet::on_exit(AppState::MainMenu)
                .with_system(close_menu)
        )
        .run();
}
It is OK to have multiple system sets for the same state.
This is useful when you want to place labels and use explicit
system ordering.
This can also be useful with Plugins. Each plugin can add
its own set of systems to the same state.
States are implemented using run criteria under the hood.
These special system set constructors are really just helpers to automatically
add the state management run criteria.
Controlling States
Inside of systems, you can check and control the state using the
State<T> resource:
fn play_music(
    app_state: Res<State<AppState>>,
    // ...
) {
    match app_state.current() {
        AppState::MainMenu => {
            // TODO: play menu music
        }
        AppState::InGame => {
            // TODO: play game music
        }
        AppState::Paused => {
            // TODO: play pause screen music
        }
    }
}
To change to another state:
fn enter_game(mut app_state: ResMut<State<AppState>>) {
    app_state.set(AppState::InGame).unwrap();
    // ^ this can fail if we are already in the target state
    // or if another state change is already queued
}
After the systems of the current state complete, Bevy will transition to
the next state you set.
You can do arbitrarily many state transitions in a single frame update. Bevy
will handle all of them and execute all the relevant systems (before moving
on to the next stage).
State Stack
Instead of completely transitioning from one state to another, you can also
overlay states, forming a stack.
This is how you can implement things like a "game paused" screen, or an
overlay menu, with the game world still visible / running in the background.
You can have some systems that are still running even when the state is
"inactive" (that is, in the background, with other states running on top). You
can also add one-shot systems to run when "pausing" or "resuming" the state.
In your app builder:
        // player movement only when actively playing
        .add_system_set(
            SystemSet::on_update(AppState::InGame)
                .with_system(player_movement)
        )
        // player idle animation while paused
        .add_system_set(
            SystemSet::on_inactive_update(AppState::InGame)
                .with_system(player_idle)
        )
        // animations both while paused and while active
        .add_system_set(
            SystemSet::on_in_stack_update(AppState::InGame)
                .with_system(animate_trees)
                .with_system(animate_water)
        )
        // things to do when becoming inactive
        .add_system_set(
            SystemSet::on_pause(AppState::InGame)
                .with_system(hide_enemies)
        )
        // things to do when becoming active again
        .add_system_set(
            SystemSet::on_resume(AppState::InGame)
                .with_system(reset_player)
        )
        // setup when first entering the game
        .add_system_set(
            SystemSet::on_enter(AppState::InGame)
                .with_system(setup_player)
                .with_system(setup_map)
        )
        // cleanup when finally exiting the game
        .add_system_set(
            SystemSet::on_exit(AppState::InGame)
                .with_system(despawn_player)
                .with_system(despawn_map)
        )
To manage states like this, use push/pop:
    // to go into the pause screen
    app_state.push(AppState::Paused).unwrap();
    // to go back into the game
    app_state.pop().unwrap();
(using .set as shown before replaces the active state at the top of the stack)
Known Pitfalls and Limitations
Combining with Other Run Criteria
Because states are implemented using run criteria,
they cannot be combined with other uses of run criteria, such as fixed
timestep.
If you try to add another run criteria to your system set, it would replace
Bevy's state-management run criteria! This would make the system set no
longer constrained to run as part of a state!
Consider using iyes_loopless, which does not
have such limitations.
Multiple Stages
Bevy states cannot work across multiple stages. Workarounds
are available, but they are broken and buggy.
This is a huge limitation in practice, as it greatly limits how you can use
commands. Not being able to use Commands is a big deal,
as you cannot do things like spawn entities and operate on them during the
same frame, among other important use cases.
Consider using iyes_loopless, which does not
have such limitations.
With Input
If you want to use Input<T> to trigger state transitions using
a button/key press, you need to clear the input manually by calling .reset:
fn esc_to_menu(
    mut keys: ResMut<Input<KeyCode>>,
    mut app_state: ResMut<State<AppState>>,
) {
    if keys.just_pressed(KeyCode::Escape) {
        app_state.set(AppState::MainMenu).unwrap();
        keys.reset(KeyCode::Escape);
    }
}
(note that this requires ResMut)
Not doing this can cause issues.
iyes_loopless does not have this issue.
Events
When receiving events in systems that don't run all the time, such
as during a pause state, you will miss any events that are sent during the frames
when the receiving systems are not running!
To mitigate this, you could implement a custom cleanup
strategy, to manually manage the lifetime of the relevant
event types.

### References
[[Manual Event Clearing  Unofficial Bevy Cheat Book]] [[Schedules  Unofficial Bevy Cheat Book]] [[System Order of Execution  Unofficial Bevy Cheat Book]] [[System Sets  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] [[Commands  Unofficial Bevy Cheat Book]] [[Plugins  Unofficial Bevy Cheat Book]] [[Fixed Timestep  Unofficial Bevy Cheat Book]] [[Events  Unofficial Bevy Cheat Book]] [[The App  Unofficial Bevy Cheat Book]] [[Run Criteria  Unofficial Bevy Cheat Book]] [[The page been moved to httpsbevycheatbookgithubioprogrammingsystemsetshtml]] [[Systems  Unofficial Bevy Cheat Book]] 