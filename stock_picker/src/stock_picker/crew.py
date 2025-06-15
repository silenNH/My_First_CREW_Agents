from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import SerperDevTool
from pydantic import BaseModel, Field   

class TrendingCompany(BaseModel):
    """A company that is in the news and attracting attention"""
    name: str=Field(description="Company Name")
    ticker: str = Field(description="Stock ticker symbol")
    reason: str = Field(description="Reason this company is trending in the news")


class TrendingCompanyList(BaseModel):
    """List of multiple trending companies that are in the news"""
    companies: List[TrendingCompany ]= Field(description = "List of companies trending in the news")
    
class TrendingCompanyResearch(BaseModel):
    """Detailed Research on the company"""
    name: str = Field(description="Company Name")
    market_position: str = Field(description="Current market position and competitive analysis")
    future_outlook: str = Field(description="Future perspectives and growth outlook")
    invetment_potential: str = Field(description="Invstment potential and suitability for investment")
    risks: str = Field(description="Summary of risks for Investment, e.g. debt level, liabilities etc.")

@CrewBase
class StockPicker():
    """StockPicker crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @Agent
    def trending_company_finder(self) -> Agent: 
        return Agent(config=self.agents_config["trending_company_finder"], tools=[SerperDevTool()])
        
    @Agent
    def financial_researcher(self) -> Agent: 
        return Agent(config=self.agents_config["financial_researcher"],  tools=[SerperDevTool()])
        
    @Agent
    def stock_picker(self) -> Agent: 
        return Agent(config=self.agent_config["stock_picker"])
        
        
    @task
    def find_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config["find_trending_companies"],
            output_pydantic=TrendingCompanyList,
            )