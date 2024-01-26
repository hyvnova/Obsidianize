Bevy Version:0.12(current)


Systems
Relevant official examples:
ecs_guide,
startup_system,
system_param.

Systems are pieces of functionality, which are run by Bevy. They are typically
implemented using regular Rust functions.
This is how you implement all your game logic. Each system specifies what data
it needs to access to do its thing, and Bevy will run them in parallel when
possible.
These functions can only take special parameter types,
to specify what data you need access to. If you use
unsupported parameter types in your function, you will get confusing compiler
errors!
Some of the possibilities are:

accessing resources using Res/ResMut
accessing components of entities using queries (Query)
creating/destroying entities, components, and resources using Commands (Commands)
sending/receiving events using EventWriter/EventReader

See here for a full list!
fn debug_start(
    // access resource
    start: Res<StartingLevel>
) {
    eprintln!("Starting on level {:?}", *start);
}
System parameters can be grouped into tuples (which can be nested). This is
useful for organization.
fn complex_system(
    (a, mut b): (Res<ResourceA>, ResMut<ResourceB>),
    (q0, q1, q2): (Query<(/* … */)>, Query<(/* … */)>, Query<(/* … */)>),
) {
    // …
}
Your function can have a maximum of 16 total parameters. If you need more,
group them into tuples to work around the limit. Tuples can contain up to
16 members, but can be nested indefinitely.
There is also a different kind of systems: exclusive systems.
They have full direct access to the ECS World, so you can access
any data you want and do anything, but cannot run in parallel. For most use
cases, you should use regular parallel systems.
fn reload_game(world: &mut World) {
    // ... access whatever we want from the World
}
Runtime
To run your systems, you need to add them to Bevy via the app builder:
fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        // run these only once at launch
        .add_systems(Startup, (setup_camera, debug_start))
        // run these every frame update
        .add_systems(Update, (move_player, enemies_ai))
        // ...
        .run();
}
Be careful: writing a new system fn and forgetting to add it to your app is a
common mistake! If you run your project and your new code doesn't seem to be
running, make sure you added the system!
The above is enough for simple projects.
Systems are contained in schedules. Update is the
schedule where you typically add any systems you want to run every frame.
Startup is where you typically add systems that should run
only once on app startup. There are also other possibilities.
As your project grows more complex, you might want to make use of some of the
powerful tools that Bevy offers for managing when/how your systems run, such as:
explicit ordering, run conditions, system
sets, states.

### References
[[Direct ECS World Access  Unofficial Bevy Cheat Book]] [[Entities Components  Unofficial Bevy Cheat Book]] [[Queries  Unofficial Bevy Cheat Book]] [[Schedules  Unofficial Bevy Cheat Book]] [[System Order of Execution  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] [[System Sets  Unofficial Bevy Cheat Book]] [[Commands  Unofficial Bevy Cheat Book]] [[Exclusive Systems  Unofficial Bevy Cheat Book]] [[Events  Unofficial Bevy Cheat Book]] [[States  Unofficial Bevy Cheat Book]] [[Resources  Unofficial Bevy Cheat Book]] [[The App  Unofficial Bevy Cheat Book]] [[Run Criteria  Unofficial Bevy Cheat Book]] [[List of Bevy Builtins  Unofficial Bevy Cheat Book]] [[Error adding function as system  Unofficial Bevy Cheat Book]] [[List of Bevy Builtins  Unofficial Bevy Cheat Book]] [[Intro Your Data  Unofficial Bevy Cheat Book]] 