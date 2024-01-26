Bevy Version:0.9(outdated!)


Generic Systems
Bevy systems are just plain rust functions, which means they
can be generic. You can add the same system multiple times, parametrized to
work on different Rust types or values.
Generic over Component types
You can use the generic type parameter to specify what
component types (and hence what entities)
your system should operate on.
This can be useful when combined with Bevy states.
You can do the same thing to different sets of entities depending on state.
Example: Cleanup
One straightforward use-case is for cleanup. We can make a generic cleanup
system that just despawns all entities that have a certain component
type. Then, trivially run it on exiting different states.
use bevy::ecs::component::Component;

fn cleanup_system<T: Component>(
    mut commands: Commands,
    q: Query<Entity, With<T>>,
) {
    for e in q.iter() {
        commands.entity(e).despawn_recursive();
    }
}
Menu entities can be tagged with cleanup::MenuExit, entities from the game
map can be tagged with cleanup::LevelUnload.
We can add the generic cleanup system to our state transitions, to take care
of the respective entities:
/// Marker components to group entities for cleanup
mod cleanup {
    use bevy::prelude::*;
    #[derive(Component)]
    pub struct LevelUnload;
    #[derive(Component)]
    pub struct MenuClose;
}

#[derive(Debug, Clone, Eq, PartialEq, Hash)]
enum AppState {
    MainMenu,
    InGame,
}

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .add_state(AppState::MainMenu)
        // add the cleanup systems
        .add_system_set(SystemSet::on_exit(AppState::MainMenu)
            .with_system(cleanup_system::<cleanup::MenuClose>))
        .add_system_set(SystemSet::on_exit(AppState::InGame)
            .with_system(cleanup_system::<cleanup::LevelUnload>))
        .run();
}
Using Traits
You can use this in combination with Traits, for when you need some sort of
varying implementation/functionality for each type.
Example: Bevy's Camera Projections
(this is a use-case within Bevy itself)
Bevy has a CameraProjection trait. Different
projection types like PerspectiveProjection
and OrthographicProjection implement that
trait, providing the correct logic for how to respond to resizing the window,
calculating the projection matrix, etc.
There is a generic system fn camera_system::<T: CameraProjection + Component>, which handles all the cameras with a given projection type. It
will call the trait methods when appropriate (like on window resize events).
The Bevy Cookbook Custom Camera Projection
Example shows this API in action.
Using Const Generics
Now that Rust has support for Const Generics, functions can also be
parametrized by values, not just types.
fn process_layer<const LAYER_ID: usize>(
    // system params
) {
    // do something for this `LAYER_ID`
}

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .add_system(process_layer::<1>)
        .add_system(process_layer::<2>)
        .add_system(process_layer::<3>)
        .run();
}
Note that these values are static / constant at compile-time. This can be
a severe limitation. In some cases, when you might suspect that you could
use const generics, you might realize that you actually want a runtime value.
If you need to "configure" your system by passing in some data, you could,
instead, use a Resource or Local.
Note: As of Rust 1.65, support for using enum values as const generics is
not yet stable. To use enums, you need Rust Nightly, and to enable the
experimental/unstable feature (put this at the top of your main.rs or
lib.rs):
#![feature(adt_const_params)]

### References
[[Entities Components  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] [[Local Resources  Unofficial Bevy Cheat Book]] [[States  Unofficial Bevy Cheat Book]] [[Resources  Unofficial Bevy Cheat Book]] [[Custom Camera Projection  Unofficial Bevy Cheat Book]] [[Systems  Unofficial Bevy Cheat Book]] [[Intro to ECS  Unofficial Bevy Cheat Book]] 