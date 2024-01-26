Bevy Version:0.9(outdated!)


Hierarchical (Parent/Child) Entities
Relevant official examples:
hierarchy,
parenting.

Technically, the Entities/Components themselves cannot form a
hierarchy (the ECS is a flat data structure). However,
logical hierarchies are a common pattern in games.
Bevy supports creating such a logical link between entities, to form
a virtual "hierarchy", by simply adding Parent and
Children components on the respective entities.
When using Commands to spawn entities,
Commands has methods for adding children to entities,
which automatically add the correct components:
// spawn the parent and get its Entity id
let parent = commands.spawn(MyParentBundle::default()).id();

// do the same for the child
let child = commands.spawn(MyChildBundle::default()).id();

// add the child to the parent
commands.entity(parent).push_children(&[child]);

// you can also use `with_children`:
commands.spawn(MyParentBundle::default())
    .with_children(|parent| {
        parent.spawn(MyChildBundle::default());
    });
Note that this only sets up the Parent and
Children components, and nothing else. Notably, it does not
add transforms or visibility for you.  If you
need that functionality, you need to add those components yourself, using
something like SpatialBundle.
You can despawn an entire hierarchy with a single command:
fn close_menu(
    mut commands: Commands,
    query: Query<Entity, With<MainMenuUI>>,
) {
    for entity in query.iter() {
        // despawn the entity and its children
        commands.entity(entity).despawn_recursive();
    }
}
Accessing the Parent or Children
To make a system that works with the hierarchy, you typically need two queries:

one with the components you need from the child entities
one with the components you need from the parent entities

One of the two queries should include the appropriate component, to obtain the
entity ids to use with the other one:

Parent in the child query, if you want to iterate entities
and look up their parents, or
Children in the parent query, if you want to iterate entities
and look up their children

For example, if we want to get the Transform
of cameras (Camera) that have a parent, and the
GlobalTransform of their parent:
fn camera_with_parent(
    q_child: Query<(&Parent, &Transform), With<Camera>>,
    q_parent: Query<&GlobalTransform>,
) {
    for (parent, child_transform) in q_child.iter() {
        // `parent` contains the Entity ID we can use
        // to query components from the parent:
        let parent_global_transform = q_parent.get(parent.get());

        // do something with the components
    }
}
As another example, say we are making a strategy game, and we have Units
that are children of a Squad. Say we need to make a system that works on
each Squad, and it needs some information about the children:
fn process_squad_damage(
    q_parent: Query<(&MySquadDamage, &Children)>,
    q_child: Query<&MyUnitHealth>,
) {
    // get the properties of each squad
    for (squad_dmg, children) in q_parent.iter() {
        // `children` is a collection of Entity IDs
        for &child in children.iter() {
            // get the health of each child unit
            let health = q_child.get(child);

            // do something
        }
    }
}
Transform and Visibility Propagation
If your entities represent "objects in the game world", you probably expect
the children to be affected by the parent.
Transform propagation allows children to be positioned
relative to their parent and move with it.
Visibility propagation allows children to be hidden if
you manually hide their parent.
Most Bundles that come with Bevy provide these behaviors
automatically. Check the docs for the bundles you are using.  Camera bundles,
for example, have transforms, but not visibility.
Otherwise, you can use SpatialBundle to make sure
your entities have all the necessary components.
Known Pitfalls
Despawning Child Entities
If you despawn an entity that has a parent, Bevy does not remove it from the
parent's Children.
If you then query for that parent entity's children, you will get an invaild
entity, and any attempt to manipulate it will likely lead to this error:
thread 'main' panicked at 'Attempting to create an EntityCommands for entity 7v0, which doesn't exist.'

The workaround is to manually call remove_children alongside the despawn:
    commands.entity(parent_entity).remove_children(&[child_entity]);
    commands.entity(child_entity).despawn();

### References
[[List of Bevy Builtins  Unofficial Bevy Cheat Book]] [[Transforms  Unofficial Bevy Cheat Book]] [[Queries  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] [[Commands  Unofficial Bevy Cheat Book]] [[Intro Your Data  Unofficial Bevy Cheat Book]] [[Visibility  Unofficial Bevy Cheat Book]] [[Intro to ECS  Unofficial Bevy Cheat Book]] 