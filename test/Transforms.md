Bevy Version:0.12(current)


Transforms
Relevant official examples:
transform,
translation,
rotation,
3d_rotation,
scale,
move_sprite,
parenting,
anything that spawns 2D or 3D objects.

First, a quick definition, if you are new to game development:
a Transform is what allows you to place an object in the game world. It
is a combination of the object's "translation" (position/coordinates),
"rotation", and "scale" (size adjustment).
You move objects around by modifying the translation, rotate them by modifying
the rotation, and make them larger or smaller by modifying the scale.
// To simply position something at specific coordinates
let xf_pos567 = Transform::from_xyz(5.0, 6.0, 7.0);

// To scale an object, making it twice as big in all dimensions
let xf_scale = Transform::from_scale(Vec3::splat(2.0));

// To rotate an object in 2D (Z-axis rotation) by 30°
// (angles are in radians! must convert from degrees!)
let xf_rot2d = Transform::from_rotation(Quat::from_rotation_z((30.0_f32).to_radians()));

// 3D rotations can be complicated; explore the methods available on `Quat`

// Simple 3D rotation by Euler-angles (X, Y, Z)
let xf_rot2d = Transform::from_rotation(Quat::from_euler(
    EulerRot::XYZ,
    (20.0_f32).to_radians(),
    (10.0_f32).to_radians(),
    (30.0_f32).to_radians(),
));

// Everything:
let xf = Transform::from_xyz(1.0, 2.0, 3.0)
    .with_scale(Vec3::new(0.5, 0.5, 1.0))
    .with_rotation(Quat::from_rotation_y(0.125 * std::f32::consts::PI));
Transform Components
In Bevy, transforms are represented by two components:
Transform and GlobalTransform.
Any Entity that represents an object in the game world
needs to have both. All of Bevy's built-in bundle types
include them.
If you are creating a custom entity without using those bundles,
you can use one of the following to ensure you don't miss them:

SpatialBundle for transforms + visibility
TransformBundle for just the transforms

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
Transform
Transform is what you typically work with. It is
a struct containing the translation, rotation, and scale. To read or
manipulate these values, access it from your systems using a
query.
If the entity has a parent, the Transform
component is relative to the parent. This means that the child object will
move/rotate/scale along with the parent.
fn inflate_balloons(
    mut query: Query<&mut Transform, With<Balloon>>,
    keyboard: Res<Input<KeyCode>>,
) {
    // every time the Spacebar is pressed,
    // make all the balloons in the game bigger by 25%
    if keyboard.just_pressed(KeyCode::Space) {
        for mut transform in &mut query {
            transform.scale *= 1.25;
        }
    }
}

fn throwable_fly(
    time: Res<Time>,
    mut query: Query<&mut Transform, With<ThrowableProjectile>>,
) {
    // every frame, make our projectiles fly across the screen and spin
    for mut transform in &mut query {
        // do not forget to multiply by the time delta!
        // this is required to move at the same speed regardless of frame rate!
        transform.translation.x += 100.0 * time.delta_seconds();
        transform.rotate_z(2.0 * time.delta_seconds());
    }
}
GlobalTransform
GlobalTransform represents the absolute global
position in the world.
If the entity does not have a parent, then this will match
the Transform.
The value of GlobalTransform is calculated/managed
internally by Bevy ("transform propagation").
Unlike Transform, the translation/rotation/scale are not
accessible directly. The data is stored in an optimized way (using Affine3A)
and it is possible to have complex transformations in a hierarchy that cannot
be represented as a simple transform. For example, a combination of rotation
and scale across multiple parents, resulting in shearing.
If you want to try to convert a GlobalTransform back
into a workable translation/rotation/scale representation, you can try the methods:

.translation()
.to_scale_rotation_translation() (may be invalid)
.compute_transform() (may be invalid)

Transform Propagation
The two components are synchronized by a bevy-internal system (the "transform
propagation system"), which runs in the PostUpdate
schedule.
Beware: When you mutate the Transform, the
GlobalTransform is not updated immediately. They
will be out-of-sync until the transform propagation system runs.
If you need to work with GlobalTransform
directly, you should add your
system to the PostUpdate
schedule and order it after
TransformSystem::TransformPropagate.
/// Print the up-to-date global coordinates of the player
fn debug_globaltransform(
    query: Query<&GlobalTransform, With<Player>>,
) {
    let gxf = query.single();
    debug!("Player at: {:?}", gxf.translation());
}
// the label to use for ordering
use bevy::transform::TransformSystem;

app.add_systems(PostUpdate,
    debug_globaltransform
        // we want to read the GlobalTransform after
        // it has been updated by Bevy for this frame
        .after(TransformSystem::TransformPropagate)
);
TransformHelper
If you need to get an up-to-date GlobalTransform
in a system that has to run before transform propagation,
you can use the special TransformHelper system parameter.
It allows you to compute a specific entity's
GlobalTransform immediately, on demand.
An example of where this could be useful might be a system to make
a camera follow an entity on-screen. You need to update the camera's
Transform (which means you have to do it before Bevy's
transform propagation, so it can account for the camera's new transform),
but you also need to know the current up-to-date position of the entity you
are following.
fn camera_look_follow(
    q_target: Query<Entity, With<MySpecialMarker>>,
    mut transform_params: ParamSet<(
        TransformHelper,
        Query<&mut Transform, With<MyGameCamera>>,
    )>,
) {
    // get the Entity ID we want to target
    let e_target = q_target.single();
    // compute its actual current GlobalTransform
    // (could be Err if entity doesn't have transforms)
    let Ok(global) = transform_params.p0().compute_global_transform(e_target) else {
        return;
    };
    // get camera transform and make it look at the global translation
    transform_params.p1().single_mut().look_at(global.translation(), Vec3::Y);
}
Internally, TransformHelper behaves like two
read-only queries. It needs access to the Parent
and Transform components to do its job. It would
conflict with our other &mut Transform query. That's why we have to use a
param set in the example above.
Note: if you over-use TransformHelper, it
could become a performance issue. It calculates the global transform
for you, but it does not update the data stored in the entity's
GlobalTransform. Bevy will still do the same
computation again later, during transform propagation. It leads to repetitive
work. If your system can run after transform propagation, so it can just
read the value after Bevy updates it, you should prefer to do that instead
of using TransformHelper.

### References
[[ParentChild Hierarchies  Unofficial Bevy Cheat Book]] [[List of Bevy Builtins  Unofficial Bevy Cheat Book]] [[Entities Components  Unofficial Bevy Cheat Book]] [[Queries  Unofficial Bevy Cheat Book]] [[Schedules  Unofficial Bevy Cheat Book]] [[ParamSet  Unofficial Bevy Cheat Book]] [[Bundles  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] [[System Order of Execution  Unofficial Bevy Cheat Book]] [[The App  Unofficial Bevy Cheat Book]] [[Visibility  Unofficial Bevy Cheat Book]] [[Systems  Unofficial Bevy Cheat Book]] [[Intro to ECS  Unofficial Bevy Cheat Book]] 