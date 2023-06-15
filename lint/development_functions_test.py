import ast

import gamla

from lint import development_functions


def test_detect_development_functions():
    cache_force_and_debug = """build_knowledge: Callable[
    [], Awaitable[knowledge_graph.KnowledgeGraph]] = versions_updater.cache_main_kg_force(
    gamla.compose_left(
        gamla.juxt(versions_updater.cache_kg_force(gamla.just(knowledge_graph.EMPTY_GRAPH)),  versions_updater.cache_faq_kg_force(gamla.just(knowledge_graph.EMPTY_GRAPH)), versions_updater.cache_kg_force(gamla.just(knowledge_graph.EMPTY_GRAPH))),
        gamla.debug,
        knowledge_graph.merge_graphs_nodes_by_id,
        gamla.debug,
        )
    )
        """
    slot_filling_debug = """ask_leading_question = slot_filling.require_or_no_effect(
        debug.debug(logic.complement(
            composers.compose_left_unary(search_state, _is_search_performed)
        )),
        leading_question_effect,
    )"""
    debug_breakpoint = """def create_routing_search_slot():
    ipdb.set_trace() 
    breakpoint()
    return slot_filling.debug_breakpoint(create_routing_search_slot_with_custom_inference(
    gamla.identity
))"""
    gamla.pipe(
        (cache_force_and_debug, slot_filling_debug, debug_breakpoint),
        gamla.map(
            gamla.compose_left(
                ast.parse,
                development_functions.detect,
                gamla.count
            )),
        tuple,
        gamla.assert_that(gamla.equals((4,1,4))),
    )
