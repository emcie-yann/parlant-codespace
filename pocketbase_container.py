from contextlib import AsyncExitStack

import parlant.sdk as p
from parlant.adapters.db.pocketbase_db import PocketBaseDocumentDatabase
from parlant.core.emission.event_publisher import EventPublisherFactory

EXIT_STACK = AsyncExitStack()


async def _make_session_store(container: p.Container) -> p.SessionStore:
    database = await EXIT_STACK.enter_async_context(
        PocketBaseDocumentDatabase(
            logger=container[p.Logger],
            collection_prefix="parlant_sessions",
        )
    )
    store = p.SessionDocumentStore(database=database, allow_migration=True)
    return await EXIT_STACK.enter_async_context(store)


async def _make_customer_store(container: p.Container) -> p.CustomerStore:
    database = await EXIT_STACK.enter_async_context(
        PocketBaseDocumentDatabase(
            logger=container[p.Logger],
            collection_prefix="parlant_customers",
        )
    )
    store = p.CustomerDocumentStore(
        id_generator=container[p.IdGenerator],
        database=database,
        allow_migration=True,
    )
    return await EXIT_STACK.enter_async_context(store)


async def _make_variable_store(container: p.Container) -> p.ContextVariableStore:
    database = await EXIT_STACK.enter_async_context(
        PocketBaseDocumentDatabase(
            logger=container[p.Logger],
            collection_prefix="parlant_context_variables",
        )
    )
    store = p.ContextVariableDocumentStore(
        id_generator=container[p.IdGenerator],
        database=database,
        allow_migration=True,
    )
    return await EXIT_STACK.enter_async_context(store)


async def configure_container(container: p.Container) -> p.Container:
    container = container.clone()

    session_store = await _make_session_store(container)
    container[p.SessionDocumentStore] = session_store
    container[p.SessionStore] = session_store

    customer_store = await _make_customer_store(container)
    container[p.CustomerDocumentStore] = customer_store
    container[p.CustomerStore] = customer_store

    variable_store = await _make_variable_store(container)
    container[p.ContextVariableDocumentStore] = variable_store
    container[p.ContextVariableStore] = variable_store

    container[p.EventEmitterFactory] = EventPublisherFactory(
        container[p.AgentStore],
        session_store,
    )

    return container


async def shutdown_pocketbase() -> None:
    await EXIT_STACK.aclose()