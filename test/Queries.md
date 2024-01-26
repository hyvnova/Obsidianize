Bevy Version:0.9(outdated!)


Queries
Relevant official examples:
ecs_guide.

Queries let you access components of entities.
Use the Query system parameter, where you can
specify the data you want to access, and optionally additional
filters for selecting entities.
Think of the types you put in your Query as a "specification" for selecting
what entities you want to access. Queries will match only those entities in the
ECS World that fit your specification. You are then able to access the relevant
data from individual such entities (using an Entity ID), or
iterate to access all entities that qualify.
The first type parameter for a query is the data you want to access. Use & for
shared/readonly access and &mut for exclusive/mutable access. Use Option if
the component is not required (you want to find entities with or without that
component. If you want multiple components, put them in a tuple.
fn check_zero_health(
    // access entities that have `Health` and `Transform` components
    // get read-only access to `Health` and mutable access to `Transform`
    // optional component: get access to `Player` if it exists
    mut query: Query<(&Health, &mut Transform, Option<&Player>)>,
) {
    // get all matching entities
    for (health, mut transform, player) in query.iter_mut() {
        eprintln!("Entity at {} has {} HP.", transform.translation, health.hp);

        // center if hp is zero
        if health.hp <= 0.0 {
            transform.translation = Vec3::ZERO;
        }

        if let Some(player) = player {
            // the current entity is the player!
            // do something special!
        }
    }
}
The above example used iteration to access all entities that the query could find.
To access the components from specific entity
only:
    if let Ok((health, mut transform)) = query.get_mut(entity) {
        // do something with the components
    } else {
        // the entity does not have the components from the query
    }
If you want to know the entity IDs of the entities you are accessing, you can
put the special Entity type in your query. This is useful
together with iteration, so you can identify the entities that the query found:
// add `Entity` to `Query` to get Entity IDs
fn query_entities(q: Query<(Entity, /* ... */)>) {
    for (e, /* ... */) in q.iter() {
        // `e` is the Entity ID of the entity we are accessing
    }
}
If you know that the query is expected to only ever match a single entity, you
can use single/single_mut (panic on error) or get_single/get_single_mut
(return Result). These methods ensure that there exists exactly
one candidate entity that can match your query, and will produce an error
otherwise.
fn query_player(mut q: Query<(&Player, &mut Transform)>) {
    let (player, mut transform) = q.single_mut();

    // do something with the player and its transform
}
Bundles
Queries work with individual components. If you created an entity using a
bundle, you need to query for the specific components from
that bundle that you care about.
A common beginner mistake is to query for the bundle type!
Query Filters
Add query filters to narrow down the entities you get from the query.
This is done using the second (optional) generic type parameter of the
Query type.
Note the syntax of the query: first you specify the data you want to access
(using a tuple to access multiple things), and then you add any additional
filters (can also be a tuple, to add multiple).
Use With/Without to only get entities
that have specific components.
fn debug_player_hp(
    // access the health (and optionally the PlayerName, if present), only for friendly players
    query: Query<(&Health, Option<&PlayerName>), (With<Player>, Without<Enemy>)>,
) {
    // get all matching entities
    for (health, name) in query.iter() {
        if let Some(name) = name {
            eprintln!("Player {} has {} HP.", name.0, health.hp);
        } else {
            eprintln!("Unknown player has {} HP.", health.hp);
        }
    }
}
This is useful if you don't actually care about the data stored inside these
components, but you want to make sure that your query only looks for entities
that have (or not have) them. If you want the data, then put the component in
the first part of the query (as shown previously), instead of using a filter.
Multiple filters can be combined:

in a tuple to apply all of them (AND logic)
using the Or<(…)> wrapper to detect any of them (OR logic).

(note the tuple inside)

### References
[[Entities Components  Unofficial Bevy Cheat Book]] [[Queries  Unofficial Bevy Cheat Book]] [[Bundles  Unofficial Bevy Cheat Book]] [[Introduction  Unofficial Bevy Cheat Book]] [[Entities Components  Unofficial Bevy Cheat Book]] [[Systems  Unofficial Bevy Cheat Book]] [[Intro to ECS  Unofficial Bevy Cheat Book]] 