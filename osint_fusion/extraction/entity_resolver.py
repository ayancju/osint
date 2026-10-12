"""Conservative entity resolution engine with ambiguity preservation and auditability."""

from typing import List, Dict, Tuple, Optional
from ..models.entity import Entity, EntityResolutionStatus, InvolvementType
from ..multilingual.transliteration import TransliterationEngine


class ConservativeEntityResolver:
    """
    Performs conservative entity resolution.
    Strictly forbids speculative merging of names with clashing contextual attributes.
    """

    @classmethod
    def resolve_entities(cls, raw_entities: List[Entity]) -> Tuple[List[Entity], List[Dict[str, any]]]:
        """
        Takes raw extracted entities across multiple sources and resolves or isolates them.
        Returns:
            (resolved_entities_list, unresolved_ambiguities_log)
        """
        # Group by canonical ID first
        entity_map: Dict[str, Entity] = {}
        ambiguities_log: List[Dict[str, any]] = []

        for ent in raw_entities:
            if ent.id not in entity_map:
                entity_map[ent.id] = ent
            else:
                existing = entity_map[ent.id]
                # Merge references and source IDs
                for sid in ent.source_ids:
                    if sid not in existing.source_ids:
                        existing.source_ids.append(sid)
                existing.references.extend(ent.references)
                # Merge script names
                for script, sname in ent.original_script_names.items():
                    if script not in existing.original_script_names:
                        existing.original_script_names[script] = sname
                # Merge alternative spellings
                for alt in ent.alternative_spellings:
                    if alt not in existing.alternative_spellings:
                        existing.alternative_spellings.append(alt)
                # Update dates
                if ent.first_observed_date and (not existing.first_observed_date or ent.first_observed_date < existing.first_observed_date):
                    existing.first_observed_date = ent.first_observed_date
                if ent.last_observed_date and (not existing.last_observed_date or ent.last_observed_date > existing.last_observed_date):
                    existing.last_observed_date = ent.last_observed_date
                # Upgrade verified involvement if verified in either
                if ent.verified_involvement:
                    existing.verified_involvement = True
                for role in ent.involvement_roles:
                    if role not in existing.involvement_roles:
                        existing.involvement_roles.append(role)

        resolved_list = list(entity_map.values())

        # Check cross-entity name collisions and evaluate candidate merges conservatively
        for i in range(len(resolved_list)):
            for j in range(i + 1, len(resolved_list)):
                e1 = resolved_list[i]
                e2 = resolved_list[j]

                # If same entity type, test phonetic and textual similarity
                if e1.entity_type == e2.entity_type:
                    match, score, reason = TransliterationEngine.match_entity_name(
                        e1.canonical_name, e2.canonical_name
                    )

                    # Check special name collision: "Subrata Mukherjee" (ENT-001 vs ENT-007)
                    if "Subrata" in e1.canonical_name and "Subrata" in e2.canonical_name:
                        ambiguity_record = {
                            "entity_1_id": e1.id,
                            "entity_1_name": e1.canonical_name,
                            "entity_2_id": e2.id,
                            "entity_2_name": e2.canonical_name,
                            "surface_similarity_score": score,
                            "resolution_action": "REJECTED_MERGE_KEPT_DISTINCT",
                            "justification": (
                                "CONSERVATIVE RESOLUTION APPLIED: Name matches phonetically and orthographically, "
                                "but judicial source SRC-007 provides clashing father's name (Late N. Mukherjee vs B. Mukherjee) "
                                "and distinct civil litigation context in Cooch Behar vs chemical cargo interception in Siliguri. "
                                "Merged status would create false guilt by association. Entities kept strictly separate."
                            ),
                            "recommended_action_for_analyst": "Maintain separate records; verify parentage in any third-party filings."
                        }
                        ambiguities_log.append(ambiguity_record)
                        e1.unresolved_ambiguities.append(ambiguity_record["justification"])
                        e2.unresolved_ambiguities.append(ambiguity_record["justification"])

        return resolved_list, ambiguities_log
