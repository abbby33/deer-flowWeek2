// Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
// SPDX-License-Identifier: MIT

export const playbook = {
  steps: [
    {
      description:
        "The Coordinator is responsible for engaging with the user to understand their problem and requirements.",
      activeNodes: ["Start", "Coordinator"],
      activeEdges: ["Start->Coordinator"],
      tooltipPosition: "right",
    },
    {
      description:
        "If the user's problem is clearly defined, the Coordinator will hand it over to the Planner.",
      activeNodes: ["Coordinator", "Planner"],
      activeEdges: ["Coordinator->Planner"],
      tooltipPosition: "left",
    },
    {
      description: "Awaiting human feedback to refine the plan.",
      activeNodes: ["Planner", "HumanFeedback"],
      activeEdges: ["Planner->HumanFeedback"],
      tooltipPosition: "left",
    },
    {
      description: "Updating the plan based on human feedback.",
      activeNodes: ["HumanFeedback", "Planner"],
      activeEdges: ["HumanFeedback->Planner"],
      tooltipPosition: "left",
    },
    {
      description:
        "The Research Team is responsible for conducting the core research tasks.",
      activeNodes: ["Planner", "HumanFeedback", "ResearchTeam"],
      activeEdges: [
        "Planner->HumanFeedback",
        "HumanFeedback->ResearchTeam",
        "ResearchTeam->HumanFeedback",
      ],
      tooltipPosition: "left",
    },
    {
      description:
        "The Researcher is responsible for gathering information using search and crawling tools.",
      activeNodes: ["ResearchTeam", "Researcher"],
      activeEdges: ["ResearchTeam->Researcher", "Researcher->ResearchTeam"],
      tooltipPosition: "left",
    },
    {
      description:
        "The Coder is responsible for writing Python code to solve math problems, data analysis, and more.",
      tooltipPosition: "right",
      activeNodes: ["ResearchTeam", "Coder"],
      activeEdges: ["ResearchTeam->Coder", "Coder->ResearchTeam"],
    },
    {
      description:
        "The Image Generator is responsible for creating images from text descriptions using Google's Imagen-3 model.",
      activeNodes: ["ResearchTeam", "ImageGenerator"],
      activeEdges: ["ResearchTeam->ImageGenerator", "ImageGenerator->ResearchTeam"],
      tooltipPosition: "left",
    },
    {
      description:
        "The Speech Generator converts text to natural-sounding speech using Google's Gemini TTS.",
      tooltipPosition: "right",
      activeNodes: ["ResearchTeam", "SpeechGenerator"],
      activeEdges: ["ResearchTeam->SpeechGenerator", "SpeechGenerator->ResearchTeam"],
    },
    {
      description:
        "Once the generation tasks are completed, the agents will hand over to the Planner.",
      activeNodes: ["ResearchTeam", "Planner"],
      activeEdges: ["ResearchTeam->Planner"],
      tooltipPosition: "left",
    },
    {
      description:
        "Once the research tasks are completed, the Researcher will hand over to the Planner.",
      activeNodes: ["ResearchTeam", "Planner"],
      activeEdges: ["ResearchTeam->Planner"],
      tooltipPosition: "left",
    },
    {
      description:
        "If no additional information is required, the Planner will handoff to the Reporter.",
      activeNodes: ["Reporter", "Planner"],
      activeEdges: ["Planner->Reporter"],
      tooltipPosition: "right",
    },
    {
      description:
        "The Reporter will prepare a report summarizing the results.",
      activeNodes: ["End", "Reporter"],
      activeEdges: ["Reporter->End"],
      tooltipPosition: "bottom",
    },
  ],
};
