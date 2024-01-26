Bevy Version:0.9(outdated!)


Run Criteria
Run Criteria are a mechanism for controlling if Bevy should run specific
systems, at runtime. This is how you can make functionality
that only runs under certain conditions.
Run Criteria can be applied to individual systems, system
sets, and stages.
Run Criteria are Bevy systems that return a value of type enum ShouldRun. They can accept any system
parameters, like a normal system.
This example shows how run criteria might be used to implement different
multiplayer modes:
use bevy::ecs::schedule::ShouldRun;

#[derive(Debug, PartialEq, Eq)]
#[derive(Resource)]
enum MultiplayerKind {
    Client,
    Host,
    Local,
}

fn run_if_connected(
    mode: Res<MultiplayerKind>,
    session: Res<MyNetworkSession>,
) -> ShouldRun
{
    if *mode == MultiplayerKind::Client && session.is_connected() {
        ShouldRun::Yes
    } else {
        ShouldRun::No
    }
}

fn run_if_host(
    mode: Res<MultiplayerKind>,
) -> ShouldRun
{
    if *mode == MultiplayerKind::Host || *mode == MultiplayerKind::Local {
        ShouldRun::Yes
    } else {
        ShouldRun::No
    }
}

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)

        // if we are currently connected to a server,
        // activate our client systems
        .add_system_set(
            SystemSet::new()
                .with_run_criteria(run_if_connected)
                .before("input")
                .with_system(server_session)
                .with_system(fetch_server_updates)
        )

        // if we are hosting the game,
        // activate our game hosting systems
        .add_system_set(
            SystemSet::new()
                .with_run_criteria(run_if_host)
                .before("input")
                .with_system(host_session)
                .with_system(host_player_movement)
                .with_system(host_enemy_ai)
        )

        // other systems in our game
        .add_system(smoke_particles)
        .add_system(water_animation)
        .add_system_set(
            SystemSet::new()
                .label("input")
                .with_system(keyboard_input)
                .with_system(gamepad_input)
        )
        .run();
}
Known Pitfalls
Combining Multiple Run Criteria
It is not possible to make a system that is conditional on multiple run
criteria. Bevy has a .pipe method that allows you to "chain" run criteria,
which could let you modify the output of a run criteria, but this is very
limiting in practice.
Consider using iyes_loopless. It allows you to
use any number of run conditions to control your systems, and does not prevent
you from using states or fixed timestep.
Events
When receiving events in systems that don't run every frame,
you will miss any events that are sent during the frames when the receiving
systems are not running!
To mitigate this, you could implement a custom cleanup
strategy, to manually manage the lifetime of the relevant
event types.

### References
[[Manual Event Clearing  Unofficial Bevy Cheat Book]] [[Schedules  Unofficial Bevy Cheat Book]] [[System Sets  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] [[Fixed Timestep  Unofficial Bevy Cheat Book]] [[Events  Unofficial Bevy Cheat Book]] [[States  Unofficial Bevy Cheat Book]] [[List of Bevy Builtins  Unofficial Bevy Cheat Book]] [[Systems  Unofficial Bevy Cheat Book]] 