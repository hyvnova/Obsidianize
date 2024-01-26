Bevy Version:0.12(current)


Resources
Relevant official examples:
ecs_guide.

Resources allow you to store a single global instance of some data type,
independently of entities.
Use them for data that is truly global for your app, such
as configuration / settings. Resources make it easy for you to access such data
from anywhere.

To create a new resource type, simply define a Rust struct or enum, and
derive the Resource trait, similar to
components and events.
#[derive(Resource)]
struct GoalsReached {
    main_goal: bool,
    bonus: u32,
}
Types must be unique; there can only be at most one instance of a given type. If
you might need multiple, consider using entities and components instead.
Bevy uses resources for many things. You can use these builtin
resources to access various features of the engine. They work just like your own
custom types.
Accessing Resources
To access the value of a resource from systems, use Res/ResMut:
fn my_system(
    // these will panic if the resources don't exist
    mut goals: ResMut<GoalsReached>,
    other: Res<MyOtherResource>,
    // use Option if a resource might not exist
    mut fancy: Option<ResMut<MyFancyResource>>,
) {
    if let Some(fancy) = &mut fancy {
        // TODO: do things with `fancy`
    }
    // TODO: do things with `goals` and `other`
}
Managing Resources
If you need to create/remove resources at runtime, you can do so using
commands (Commands):
fn my_setup(mut commands: Commands, /* ... */) {
    // add (or overwrite) resource, using the provided data
    commands.insert_resource(GoalsReached { main_goal: false, bonus: 100 });
    // ensure resource exists (creating if necessary)
    commands.init_resource::<MyFancyResource>();
    // remove a resource (if it exists)
    commands.remove_resource::<MyOtherResource>();
}
Alternatively, using direct World access from an exclusive
system:
fn my_setup2(world: &mut World) {
    // The same methods as with Commands are also available here,
    // but we can also do fancier things:

    // Check if resource exists
    if !world.contains_resource::<MyFancyResource>() {
        // Get access to a resource, inserting a custom value if unavailable
        let _bonus = world.get_resource_or_insert_with(
            || GoalsReached { main_goal: false, bonus: 100 }
        ).bonus;
    }
}
Resources can also be set up from the app builder. Do this for
resources that are meant to always exist from the start.
App::new()
    .add_plugins(DefaultPlugins)
    .insert_resource(StartingLevel(3))
    .init_resource::<MyFancyResource>()
    // ...
Resource Initialization
Implement Default for simple resources:
// simple derive, to set all fields to their defaults
#[derive(Resource, Default)]
struct GameProgress {
    game_completed: bool,
    secrets_unlocked: u32,
}

#[derive(Resource)]
struct StartingLevel(usize);

// custom implementation for unusual values
impl Default for StartingLevel {
    fn default() -> Self {
        StartingLevel(1)
    }
}

// on enums, you can specify the default variant
#[derive(Resource, Default)]
enum GameMode {
    Tutorial,
    #[default]
    Singleplayer,
    Multiplayer,
}
For resources that need complex initialization, implement FromWorld:
#[derive(Resource)]
struct MyFancyResource { /* stuff */ }

impl FromWorld for MyFancyResource {
    fn from_world(world: &mut World) -> Self {
        // You have full access to anything in the ECS World from here.
        // For example, you can access (and mutate!) other resources:
        let mut x = world.resource_mut::<MyOtherResource>();
        x.do_mut_stuff();

        MyFancyResource { /* stuff */ }
    }
}
Beware: it can be easy to get yourself into a mess of unmaintainable code
if you overuse FromWorld to do complex things.
Usage Advice
The choice of when to use entities/components vs. resources is
typically about how you want to access the data: globally
from anywhere (resources), or using ECS patterns (entities/components).
Even if there is only one of a certain thing in your game (such as the
player in a single-player game), it can be a good fit to use an entity
instead of resources, because entities are composed of multiple components,
some of which can be common with other entities. This can make your game
logic more flexible. For example, you could have a "health/damage system"
that works with both the player and enemies.
Settings
One common usage of resources is for storing settings and configuration.
However, if it is something that cannot be changed at runtime and only used when
initializing a plugin, consider putting that inside the plugin's
struct, instead of a resource.
Caches
Resources are also useful if you want to store some data in a way that is easier
or more efficient for you to access. For example, keeping a collection of asset
handles, or using a custom datastructure for representing a game
map more efficiently than using entities and components, etc.
Entities and Components, as flexible as they are, are not necessarily
the best fit for all use cases. If you want to represent your data some other
way, feel free to do so. Simply create a resource and put it there.
Interfacing with external libraries
If you want to integrate some external non-Bevy software into a Bevy app,
it can be very convenient to create a resource to hold onto its state/data.
For example, if you wanted to use an external physics or audio engine, you
could put all its data in a resource, and write some systems to call its
functions. That can give you an easy way to interface with it from Bevy code.
If the external code is not thread-safe (!Send in Rust parlance), which is
common for non-Rust (e.g C++ and OS-level) libraries, you should use a
Non-Send Bevy resource instead. This will make sure any Bevy
system that touches it will run on the main thread.

### References
[[Direct ECS World Access  Unofficial Bevy Cheat Book]] [[Entities Components  Unofficial Bevy Cheat Book]] [[List of Bevy Builtins  Unofficial Bevy Cheat Book]] [[Handles  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] [[Intro Your Data  Unofficial Bevy Cheat Book]] [[Commands  Unofficial Bevy Cheat Book]] [[Plugins  Unofficial Bevy Cheat Book]] [[Exclusive Systems  Unofficial Bevy Cheat Book]] [[Events  Unofficial Bevy Cheat Book]] [[NonSend  Unofficial Bevy Cheat Book]] [[The App  Unofficial Bevy Cheat Book]] [[Systems  Unofficial Bevy Cheat Book]] [[Intro Your Data  Unofficial Bevy Cheat Book]] 