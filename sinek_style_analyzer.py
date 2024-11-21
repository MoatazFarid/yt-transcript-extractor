import openai
import time
from typing import List, Dict, Optional
from dataclasses import dataclass
from openai import OpenAI
import os

@dataclass
class Point:
    main_point: str
    sub_points: List[str]
    content: Optional[str] = None

class SinekStyleAnalyzer:
    def __init__(self, api_key: str, model: str = "gpt-4", max_retries: int = 5, initial_wait_time: int = 2):
        """Initialize the analyzer with OpenAI credentials and configuration."""
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.max_retries = max_retries
        self.initial_wait_time = initial_wait_time

    def _api_call_with_retry(self, messages: List[Dict[str, str]]) -> str:
        """Make an API call with retries on failure."""
        retries = 0
        wait_time = self.initial_wait_time
        
        while retries < self.max_retries:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"API call failed: {str(e)}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                retries += 1
                wait_time *= 2
        raise Exception("Max retries reached. Exiting.")

    def process_transcript(self, transcript: str, chunk_size: int = 1000) -> List[Point]:
        """Process transcript and return structured points."""
        chunks = [transcript[i:i+chunk_size] for i in range(0, len(transcript), chunk_size)]
        points: List[Point] = []
        main_point_count = 0

        for chunk in chunks:
            messages = [
                {"role": "system", "content": "You are a helpful assistant that analyzes content in Simon Sinek's style."},
                {"role": "user", "content": f"Starting from point {main_point_count + 1}, analyze this text and extract main points and sub-points:\n\n{chunk}"}
            ]
            
            response = self._api_call_with_retry(messages)
            chunk_points = self._parse_points(response)
            points.extend(chunk_points)
            main_point_count += len(chunk_points)
            time.sleep(1)  # Rate limiting

        return points

    def _parse_points(self, response: str) -> List[Point]:
        """Parse the response into structured points."""
        points = []
        current_point = None
        
        for line in response.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            if line[0].isdigit() and '.' in line:
                # Main point
                if current_point:
                    points.append(current_point)
                main_point = line[line.find('.')+1:].strip()
                current_point = Point(main_point=main_point, sub_points=[])
            elif line.count('.') > 1 and line[0].isdigit():
                # Sub point
                if current_point:
                    sub_point = line[line.rfind('.')+1:].strip()
                    current_point.sub_points.append(sub_point)
        
        if current_point:
            points.append(current_point)
        
        return points

    def generate_detailed_content(self, points: List[Point]) -> List[Point]:
        """Generate detailed content for each point in Simon Sinek's style."""
        for point in points:
            messages = [
                {"role": "system", "content": "You are Simon Sinek, explaining concepts in your characteristic style."},
                {"role": "user", "content": f"Elaborate on this point and its sub-points in your style:\n\nMain point: {point.main_point}\nSub-points: {', '.join(point.sub_points)}"}
            ]
            
            detailed_content = self._api_call_with_retry(messages)
            point.content = detailed_content
            time.sleep(1)  # Rate limiting
        
        return points

    def save_to_file(self, points: List[Point], output_file: str = "output.txt"):
        """Save the analyzed content to a file."""
        with open(output_file, "w", encoding='utf-8') as file:
            for point in points:
                file.write(f"# {point.main_point}\n\n")
                for sub_point in point.sub_points:
                    file.write(f"## {sub_point}\n\n")
                if point.content:
                    file.write(f"{point.content}\n\n")
                file.write("-" * 80 + "\n\n")

def create_analyzer(api_key: str, **kwargs) -> SinekStyleAnalyzer:
    """Factory function to create a SinekStyleAnalyzer instance."""
    return SinekStyleAnalyzer(api_key, **kwargs) 