Bevy Version:0.12(current)


Visibility
Relevant official examples:
parenting.

Visibility is used to control if something is to be rendered or not. If you
want an entity to exist in the world, just not be displayed, you can hide it.
/// Prepare the game map, but do not display it until later
fn setup_map_hidden(
    mut commands: Commands,
) {
    commands.spawn((
        GameMapEntity,
        SceneBundle {
            scene: todo!(),
            visibility: Visibility::Hidden,
            ..Default::default()
        },
    ));
}

/// When everything is ready, un-hide the game map
fn reveal_map(
    mut query: Query<&mut Visibility, With<GameMapEntity>>,
) {
    let mut vis_map = query.single_mut();
    *vis_map = Visibility::Visible;
}
Visibility Components
In Bevy, visibility is represented by multiple components:

Visibility: the user-facing toggle (here is where you set what you want)
InheritedVisibility: used by Bevy to keep track of the state from any parent entities
ViewVisibility: used by Bevy to track if the entity should actually be displayed

Any Entity that represents a renderable object in
the game world needs to have them all. All of Bevy's built-in bundle
types include them.
If you are creating a custom entity without using those bundles,
you can use one of the following to ensure you don't miss them:

SpatialBundle for transforms + visibility
VisibilityBundle for just visibility

fn spawn_special_entity(
    mut commands: Commands,
) {
    // create an entity that does not use one of the common Bevy bundles,
    // but still needs transforms and visibility
    commands.spawn((
        ComponentA,
        ComponentB,
        SpatialBundle {
            transform: Transform::from_scale(Vec3::splat(3.0)),
            visibility: Visibility::Hidden,
            ..Default::default()
        },
    ));
}
If you don't do this correctly (say, you manually add just the Visibility
component and forget the others, because you don't use a bundle), your
entities will not render!
Visibility
Visibility is the "user-facing toggle". This is where
you specify what you want for the current entity:

Inherited (default): show/hide depending on parent
Visible: always show the entity, regardless of parent
Hidden: always hide the entity, regardless of parent

If the current entity has any children that have Inherited,
their visibility will be affected if you set the current entity to Visible
or Hidden.
If an entity has a parent, but the parent entity is missing the
visibility-related components, things will behave as if there was no parent.
InheritedVisibility
InheritedVisibility represents the state the
current entity would have based on its parent's visibility.
The value of InheritedVisibility should
be considered read-only. It is managed internally by Bevy, in a manner
similar to transform propagation. A "visibility
propagation" system runs in the PostUpdate
schedule.
If you want to read the up-to-date value for the current frame, you should
add your system to the PostUpdate
schedule and order it after
VisibilitySystems::VisibilityPropagate.
/// Check if a specific UI button is visible
/// (could be hidden if the whole menu is hidden?)
fn debug_player_visibility(
    query: Query<&InheritedVisibility, With<MyAcceptButton>>,
) {
    let vis = query.single();

    debug!("Button visibility: {:?}", vis.get());
}
use bevy::render::view::VisibilitySystems;

app.add_systems(PostUpdate,
    debug_player_visibility
        .after(VisibilitySystems::VisibilityPropagate)
);
ViewVisibility
ViewVisibility represents the actual final
decision made by Bevy about whether this entity needs to be rendered.
The value of ViewVisibility is read-only. It
is managed internally by Bevy.
It is used for "culling": if the entity is not in the range of
any Camera or Light, it does not need to be rendered, so Bevy will hide it
to improve performance.
Every frame, after "visibility propagation", Bevy will check what entities
can be seen by what view (camera or light), and store the outcome in these
components.
If you want to read the up-to-date value for the current frame, you should
add your system to the PostUpdate
schedule and order it after
VisibilitySystems::CheckVisibility.
/// Check if balloons are seen by any Camera, Light, etc… (not culled)
fn debug_balloon_visibility(
    query: Query<&ViewVisibility, With<Balloon>>,
) {
    for vis in query.iter() {
        if vis.get() {
            debug!("Balloon will be rendered.");
        }
    }
}
use bevy::render::view::VisibilitySystems;

app.add_systems(PostUpdate,
    debug_balloon_visibility
        .after(VisibilitySystems::CheckVisibility)
);

### References
[[ParentChild Hierarchies  Unofficial Bevy Cheat Book]] [[List of Bevy Builtins  Unofficial Bevy Cheat Book]] [[Transforms  Unofficial Bevy Cheat Book]] [[Entities Components  Unofficial Bevy Cheat Book]] [[Transforms  Unofficial Bevy Cheat Book]] [[Schedules  Unofficial Bevy Cheat Book]] [[Bundles  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] [[System Order of Execution  Unofficial Bevy Cheat Book]] [[The App  Unofficial Bevy Cheat Book]] [[Systems  Unofficial Bevy Cheat Book]] [[Intro to ECS  Unofficial Bevy Cheat Book]] 