from typing import List, Dict, Any

class ConfidenceScoringService:
    @staticmethod
    def get_source_type(url: str, default: str = "News Source") -> str:
        """Dynamically detect source type based on URL keywords."""
        if not url or url == "Public information unavailable":
            return "Not Found"
        url_lower = url.lower()
        if "linkedin.com" in url_lower:
            return "LinkedIn"
        if any(keyword in url_lower for keyword in ["event", "expo", "summit", "conference", "show", "ticket", "register", "meetup"]):
            return "Public Event Site"
        if any(keyword in url_lower for keyword in ["news", "press", "blog", "wire", "report", "article", "prnewswire", "venturebeat", "techcrunch"]):
            return "News Source"
        return "Official Website"

    @staticmethod
    def get_confidence_label(score: Any) -> str:
        """Map numeric score (1-100 or 0-1) to HIGH/MEDIUM/LOW."""
        try:
            val = float(score)
            if val > 1.0: # 1-100 scale
                if val >= 80: return "HIGH"
                if val >= 50: return "MEDIUM"
                return "LOW"
            else: # 0-1 scale
                if val >= 0.8: return "HIGH"
                if val >= 0.5: return "MEDIUM"
                return "LOW"
        except (ValueError, TypeError):
            if str(score).upper() in ["HIGH", "MEDIUM", "LOW"]:
                return str(score).upper()
            return "MEDIUM"

    @classmethod
    def score_and_rank(cls, brands: List[Dict[str, Any]], events: List[Dict[str, Any]], 
                       contacts: List[Dict[str, Any]], activities: List[Dict[str, Any]], 
                       outreach: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Rank prospects based on formula and attach source visibility details.
        """
        scored_brands = []
        for b in brands:
            # Enforce numeric types safely
            try:
                sf = float(b.get("strategic_fit_score", 70))
            except: sf = 70.0
            
            try:
                gs = float(b.get("growth_signal_score", 70))
            except: gs = 70.0
            
            try:
                ep = float(b.get("event_presence_score", 70))
            except: ep = 70.0
            
            try:
                ra = float(b.get("recent_activity_score", 70))
            except: ra = 70.0

            # Formula: 0.35 * strategic_fit + 0.25 * recent_activity + 0.20 * growth_signal + 0.20 * event_presence
            overall_score = (0.35 * sf) + (0.25 * ra) + (0.20 * gs) + (0.20 * ep)
            overall_score = round(overall_score, 1)

            # Map confidence & source metadata
            source_url = b.get("source_url") or "https://google.com"
            confidence_val = b.get("confidence_score") or 80
            
            scored_brands.append({
                **b,
                "strategic_fit_score": int(sf),
                "growth_signal_score": int(gs),
                "event_presence_score": int(ep),
                "recent_activity_score": int(ra),
                "overall_score": overall_score,
                "confidence_label": cls.get_confidence_label(confidence_val),
                "source_type": cls.get_source_type(source_url),
                "source_url": source_url
            })

        # Rank by overall_score descending
        ranked_prospects = sorted(scored_brands, key=lambda x: x.get("overall_score", 0), reverse=True)

        # Annotate events
        annotated_events = []
        for ev in events:
            url = ev.get("official_url") or ev.get("source_url") or ""
            annotated_events.append({
                **ev,
                "confidence_label": cls.get_confidence_label(ev.get("confidence_score") or "HIGH"),
                "source_type": cls.get_source_type(url, "Public Event Site"),
                "source_url": url or "Public information unavailable"
            })

        # Annotate contacts
        annotated_contacts = []
        for c in contacts:
            url = c.get("source_url") or c.get("linkedin") or ""
            annotated_contacts.append({
                **c,
                "confidence_label": cls.get_confidence_label(c.get("confidence_score") or "MEDIUM"),
                "source_type": cls.get_source_type(url, "LinkedIn"),
                "source_url": url or "Public information unavailable"
            })

        # Annotate activities
        annotated_activities = []
        for act in activities:
            url = act.get("source_url") or ""
            annotated_activities.append({
                **act,
                "confidence_label": cls.get_confidence_label(act.get("confidence_score") or "HIGH"),
                "source_type": cls.get_source_type(url, "News Source"),
                "source_url": url or "Public information unavailable"
            })

        return {
            "prospects": ranked_prospects,
            "events": annotated_events,
            "contacts": annotated_contacts,
            "activities": annotated_activities,
            "outreach": outreach
        }
