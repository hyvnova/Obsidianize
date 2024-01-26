Bevy Version:0.9(outdated!)


Commands
Relevant official examples:
ecs_guide.

Use Commands to spawn/despawn entities, add/remove
components on existing entities, manage resources.
These actions do not take effect immediately; they are queued to be performed
later when it is safe to do so. See: stages.
(if you are not using stages, that means your other systems
will see them on the next frame update)
fn spawn_things(
    mut commands: Commands,
) {
    // manage resources
    commands.insert_resource(MyResource);
    commands.remove_resource::<MyResource>();

    // create a new entity using `spawn`,
    // providing the data for the components it should have
    // (typically using a Bundle)
    commands.spawn(PlayerBundle {
        name: PlayerName("Henry".into()),
        xp: PlayerXp(1000),
        health: Health {
            hp: 100.0, extra: 20.0
        },
        _p: Player,
        sprite: Default::default(),
    });

    // you can use a tuple if you need additional components or bundles
    // (tuples of component and bundle types are considered bundles)
    // (note the extra parentheses)
    let my_entity_id = commands.spawn((
        // add some components
        ComponentA,
        ComponentB::default(),
        // add some bundles
        MyBundle::default(),
        TransformBundle::default(),
    )).id(); // get the Entity (id) by calling `.id()` at the end

    // add/remove components of an existing entity
    commands.entity(my_entity_id)
        .insert(ComponentC::default())
        .remove::<ComponentA>()
        .remove::<(ComponentB, MyBundle)>();
}

fn make_all_players_hostile(
    mut commands: Commands,
    // we need the Entity id, to perform commands on specific entities
    query: Query<Entity, With<Player>>,
) {
    for entity in query.iter() {
        commands.entity(entity)
            // add an `Enemy` component to the entity
            .insert(Enemy)
            // remove the `Friendly` component
            .remove::<Friendly>();
    }
}

fn despawn_all_enemies(
    mut commands: Commands,
    query: Query<Entity, With<Enemy>>,
) {
    for entity in query.iter() {
        commands.entity(entity).despawn();
    }
}

### References
[[Schedules  Unofficial Bevy Cheat Book]] [[Systems  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] 