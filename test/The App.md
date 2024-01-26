Bevy Version:0.12(current)


The App
Relevant official examples: All of them ;)
In particular, check out the complete game examples:
alien_cake_addict,
breakout.

To enter the Bevy runtime, you need to configure an App. The app
is how you define the structure of all the things that make up your project:
plugins, systems (and their configuration/metadata:
run conditions, ordering, sets),
event types, states, schedules…
You typically create your App in your project's main function.
However, you don't have to add everything from there. If you want to add things
to your app from multiple places (like other Rust files or crates), use
plugins. As your project grows, you will need to do that to keep
everything organized.
fn main() {
    App::new()
        // Bevy itself:
        .add_plugins(DefaultPlugins)

        // events:
        .add_event::<LevelUpEvent>()

        // systems to run once at startup:
        .add_systems(Startup, spawn_things)

        // systems to run each frame:
        .add_systems(Update, (
            player_level_up,
            debug_levelups,
            debug_stats_change,
        ))
        // ...

        // launch the app!
        .run();
}
Note: use tuples with add_systems/add_plugins/configure_sets to add
multiple things at once.
Component types do not need to be registered.
Schedules cannot (yet) be modified at runtime; all
systems you want to run must be added/configured in the
App ahead of time. You can control individual systems using run
conditions. You can also dynamically enable/disable entire
schedules using the
MainScheduleOrder resource.
Builtin Bevy Functionality
The Bevy game engine's own functionality is represented as a plugin group.
Every typical Bevy app must first add it, using either:

DefaultPlugins if you are making a full game/app
MinimalPlugins for something like a headless server.

Setting up data
Normally, you can set up your data from
systems. Use Commands from regular systems, or
use exclusive systems to get full World access.
Add your setup systems as startup systems for things you want to initialize
at launch, or use state enter/exit systems to do things when
transitioning between menus, game modes, levels, etc.
However, you can also initialize data directly from the app builder. This
is common for resources, if they need to be present at all
times. You can also get direct World access.
// Create (or overwrite) resource with specific value
app.insert_resource(StartingLevel(3));

// Ensure resource exists; if not, create it
// (using `Default` or `FromWorld`)
app.init_resource::<MyFancyResource>();

// We can also access/manipulate the World directly
// (in this example, to spawn an entity, but you can do anything)
app.world.spawn(SomeBundle::default());
Quitting the App
To cleanly shut down bevy, send an AppExit
event from any system:
use bevy::app::AppExit;

fn exit_system(mut exit: EventWriter<AppExit>) {
    exit.send(AppExit);
}
For prototyping, Bevy provides a convenient system you can add, to close the
focused window on pressing the Esc key. When all windows are closed, Bevy will
quit automatically.
app.add_systems(Update, bevy::window::close_on_esc);

### References
[[Direct ECS World Access  Unofficial Bevy Cheat Book]] [[Entities Components  Unofficial Bevy Cheat Book]] [[Plugins  Unofficial Bevy Cheat Book]] [[Schedules  Unofficial Bevy Cheat Book]] [[System Order of Execution  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] [[System Sets  Unofficial Bevy Cheat Book]] [[Commands  Unofficial Bevy Cheat Book]] [[Plugins  Unofficial Bevy Cheat Book]] [[Exclusive Systems  Unofficial Bevy Cheat Book]] [[Events  Unofficial Bevy Cheat Book]] [[States  Unofficial Bevy Cheat Book]] [[Resources  Unofficial Bevy Cheat Book]] [[Run Criteria  Unofficial Bevy Cheat Book]] [[]] [[Systems  Unofficial Bevy Cheat Book]] [[Intro Your Data  Unofficial Bevy Cheat Book]] 