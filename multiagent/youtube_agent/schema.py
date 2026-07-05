from pydantic import BaseModel, Field
from typing import List

# schemas for reporter agent.

class Quickstat(BaseModel):
    label: str = Field(description="KPI label (e.g., 'Core Framework', 'Main Problem', 'Target Audience').")
    value: str = Field(description="1-3 word highlight value.")

class ChapterMilestone(BaseModel):
    timestamp: str = Field(description="The timestamp string from the video (e.g., '03:45').")
    chapter_title: str = Field(description="A concise, punchy title for this specific section.")
    summary: str = Field(description="A brief and crisp summary of what is taught in this section. summary should not extend 3 sentences.")

class ContextAwareQA(BaseModel):
    question: str = Field(description="A sharp, relevant question a user would ask about the complex core topics of this specific video.")
    answer: str = Field(description="A high-quality, comprehensive answer derived directly from the deep context of the transcript.")

class VedioSummary(BaseModel):
    vedio_summary:str =Field(description="Generate a A high-impact, 2-sentence overview of the video's core value proposition.")
    quick_states: List[Quickstat]=Field(description="Exactly 3 key technical details or high-level meta-data points for a top grid component.")
    interactive_timeline: List[ChapterMilestone]=Field(description="Chronological breakdown of the video to populate a clickable timeline component.")
    actionable_takeaways: List[str] = Field(description="Top 5 sharp, developer-focused actionable bullets from the transcript.")
    context_aware_faq: List[ContextAwareQA] = Field(description="Exactly 3 high-value, predictive FAQ pairs explaining the most complex concepts from the content.")


