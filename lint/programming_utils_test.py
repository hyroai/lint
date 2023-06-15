import ast

import gamla

from lint import programming_utils


def test_detect_programming_utils():
    gamla.pipe(
        """build_knowledge: Callable[
    [], Awaitable[knowledge_graph.KnowledgeGraph]
] = versions_updater.cache_main_kg_force(
    gamla.compose_left(
        gamla.juxt(_build_providers_kg, _build_faq_kg, _build_site_search_kg),
        gamla.debug,
        knowledge_graph.merge_graphs_nodes_by_id,))""",
        ast.parse,
        programming_utils.detect,
        gamla.assert_that(gamla.len_equals(2)),
    )
