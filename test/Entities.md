Bevy Version:0.12(current)


Relevant official examples:
ecs_guide.

Entities
See here for more explanation on how storing data in the ECS works.
Conceptually, an entity represents a set of values for different components.
Each component is a Rust type (struct or enum) and an entity can be used to
store a value of that type.
Technically, an entity is just a simple integer ID (imagine the "row number" in
a table/spreadsheet) that can be used to find related data values (in different
"columns" of that table).
In Bevy, Entity is this value. It consists of two integers:
the ID and the "generation" (allowing IDs to be reused, after you despawn old
entities).
You can create ("spawn") new entities and destroy ("despawn") entities using
Commands or exclusive World access.
fn setup(mut commands: Commands) {
    // create a new entity
    commands.spawn((
        // Initialize all your components and bundles here
        Enemy,
        Health {
            hp: 100.0,
            extra: 25.0,
        },
        AiMode::Passive,
        // ...
    ));

    // If you want to get the Entity ID, just call `.id()` after spawn
    let my_entity = commands.spawn((/* ... */)).id();

    // destroy an entity, removing all data associated with it
    commands.entity(my_entity).despawn();
}
Many of your entities might need to have the same common components. You can use
Bundles to make it easier to spawn your entities.
Components
Components are the data associated with entities.
To create a new component type, simply define a Rust struct or enum, and
derive the Component trait.
#[derive(Component)]
struct Health {
    hp: f32,
    extra: f32,
}

#[derive(Component)]
enum AiMode {
    Passive,
    ChasingPlayer,
}
Types must be unique – an entity can only have one component per Rust type.
Newtype Components
Use wrapper (newtype) structs to make unique components out of simpler types:
#[derive(Component)]
struct PlayerXp(u32);

#[derive(Component)]
struct PlayerName(String);
Marker Components
You can use empty structs to help you identify specific entities. These are
known as "marker components". Useful with query filters.
/// Add this to all menu ui entities to help identify them
#[derive(Component)]
struct MainMenuUI;

/// Marker for hostile game units
#[derive(Component)]
struct Enemy;

/// This will be used to identify the main player entity
#[derive(Component)]
struct Player;

/// Tag all creatures that are currently friendly towards the player
#[derive(Component)]
struct Friendly;
Accessing Components
Components can be accessed from systems, using queries.
You can think of the query as the "specification" for the data you want to access.
It will search for entities that match and give you access to the data.
fn level_up_player(
    // get the relevant data. some components read-only, some mutable
    mut query_player: Query<(&PlayerName, &mut PlayerXp, &mut Health), With<Player>>,
) {
    // `single` assumes only one entity exists that matches the query
    let (name, mut xp, mut health) = query_player.single_mut();
    if xp.0 > 1000 {
        xp.0 = 0;
        health.hp = 100.0;
        health.extra += 25.0;
        info!("Player {} leveled up!", name.0);
    }
}

fn die(
    // `Entity` can be used to get the ID of things that match the query
    query_health: Query<(Entity, &Health)>,
    // we also need Commands, so we can despawn entities if we have to
    mut commands: Commands,
) {
    // we can have many such entities (enemies, player, whatever)
    // so we loop to check all of them
    for (entity_id, health) in query_health.iter() {
        if health.hp <= 0.0 {
            commands.entity(entity_id).despawn();
        }
    }
}
Adding/removing Components
You can add/remove components on existing entities, using Commands or
exclusive World access.
fn make_enemies_friendly(
    query_enemy: Query<Entity, With<Enemy>>,
    mut commands: Commands,
) {
    for entity_id in query_enemy.iter() {
        commands.entity(entity_id)
            .remove::<Enemy>()
            .insert(Friendly);
    }
}

### References
[[Direct ECS World Access  Unofficial Bevy Cheat Book]] [[Queries  Unofficial Bevy Cheat Book]] [[Queries  Unofficial Bevy Cheat Book]] [[Bundles  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] [[Commands  Unofficial Bevy Cheat Book]] [[Systems  Unofficial Bevy Cheat Book]] [[Intro Your Data  Unofficial Bevy Cheat Book]] 