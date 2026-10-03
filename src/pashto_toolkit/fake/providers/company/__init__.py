"""Base company provider."""

from typing import Sequence

from ...core import BaseProvider


class Provider(BaseProvider):
    """Company names, legal suffixes and marketing filler.

    ``catch_phrase()`` and ``bs()`` draw on English business jargon in both
    locales; no Pashto equivalents are invented here.
    """

    formats: Sequence[str] = ("{{last_name}} {{company_suffix}}",)
    companies: Sequence[str] = ()
    company_suffixes: Sequence[str] = ("Ltd", "Group", "Company")

    catch_phrase_adjectives: Sequence[str] = (
        "Adaptive", "Advanced", "Balanced", "Centralized", "Compatible", "Configurable",
        "Cross-platform", "Decentralized", "Devolved", "Digitized", "Distributed",
        "Diverse", "Enterprise-wide", "Extended", "Integrated", "Intuitive", "Managed",
        "Networked", "Open-source", "Optimized", "Persistent", "Reactive", "Robust",
        "Scalable", "Secured", "Streamlined", "Sustainable", "Synergistic", "Universal",
    )
    catch_phrase_nouns: Sequence[str] = (
        "access", "architecture", "capability", "capacity", "database", "framework",
        "functionality", "infrastructure", "interface", "methodology", "middleware",
        "migration", "model", "monitoring", "paradigm", "platform", "portal",
        "productivity", "service-desk", "solution", "strategy", "structure", "toolset",
    )
    catch_phrase_descriptors: Sequence[str] = (
        "24/7", "24-hour", "actuating", "analyzing", "asymmetric", "background",
        "bi-directional", "bottom-line", "clear-thinking", "client-driven", "composite",
        "context-sensitive", "dynamic", "executive", "global", "heuristic", "hybrid",
        "local", "logistical", "mission-critical", "modular", "multi-tasking",
        "national", "needs-based", "optimal", "regional", "stable", "static",
    )
    bs_verbs: Sequence[str] = (
        "aggregate", "architect", "benchmark", "brand", "cultivate", "deliver",
        "deploy", "disintermediate", "drive", "e-enable", "embrace", "empower",
        "enable", "engage", "enhance", "evolve", "expedite", "facilitate", "generate",
        "harness", "implement", "incentivize", "innovate", "integrate", "iterate",
        "leverage", "matrix", "maximize", "monetize", "morph", "optimize",
        "orchestrate", "productize", "reinvent", "repurpose", "scale", "seize",
        "streamline", "syndicate", "synergize", "target", "transform", "unleash",
    )
    bs_adjectives: Sequence[str] = (
        "24/365", "24/7", "B2B", "B2C", "back-end", "best-of-breed", "bleeding-edge",
        "bricks-and-clicks", "clicks-and-mortar", "collaborative", "compelling",
        "cross-media", "cross-platform", "customized", "cutting-edge", "distributed",
        "dot-com", "dynamic", "e-business", "efficient", "end-to-end", "enterprise",
        "extensible", "frictionless", "front-end", "global", "granular", "holistic",
        "impactful", "innovative", "integrated", "interactive", "intuitive",
        "killer", "leading-edge", "magnetic", "mission-critical", "next-generation",
        "one-to-one", "open-source", "out-of-the-box", "plug-and-play", "proactive",
        "real-time", "revolutionary", "rich", "robust", "scalable", "seamless",
        "sexy", "sticky", "strategic", "synergistic", "transparent", "turn-key",
        "ubiquitous", "user-centric", "value-added", "vertical", "viral", "virtual",
        "visionary", "web-enabled", "wireless", "world-class",
    )
    bs_nouns: Sequence[str] = (
        "ROI", "action-items", "applications", "architectures", "bandwidth",
        "channels", "communities", "content", "convergence", "deliverables",
        "e-business", "e-commerce", "e-markets", "e-services", "e-tailers",
        "experiences", "eyeballs", "functionalities", "infomediaries",
        "infrastructures", "initiatives", "interfaces", "markets", "methodologies",
        "metrics", "mindshare", "models", "networks", "niches", "paradigms",
        "partnerships", "platforms", "portals", "relationships", "schemas",
        "solutions", "supply-chains", "synergies", "systems", "technologies",
        "users", "web-readiness", "web-services",
    )

    def company(self) -> str:
        if self.companies:
            return self.random_element(self.companies)
        return self.parse(self.random_element(self.formats))

    def company_suffix(self) -> str:
        return self.random_element(self.company_suffixes)

    def catch_phrase(self) -> str:
        return " ".join(
            (
                self.random_element(self.catch_phrase_adjectives),
                self.random_element(self.catch_phrase_descriptors),
                self.random_element(self.catch_phrase_nouns),
            )
        )

    def bs(self) -> str:
        return " ".join(
            (
                self.random_element(self.bs_verbs),
                self.random_element(self.bs_adjectives),
                self.random_element(self.bs_nouns),
            )
        )
