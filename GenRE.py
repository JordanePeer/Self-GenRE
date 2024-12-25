import csv
import os
import openai

def get_user_input():
    """Get project details from the user."""
    project_name = input("What is the name of the project? ")
    project_summary = input("Provide a short explanation about the project: ")
    csv_file_path = input("Please provide the path to the initial requirements CSV file: ")
    number_requirements = input("Please provide the number of new requirements you want to generate: ")
    return project_name, project_summary, csv_file_path, number_requirements

def upload_module(file):
    """Upload and parse the requirements CSV file."""
    with open(file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip header

        requirements = []
        for row in csv_reader:
            requirements.append(row[1])

    return requirements

def generate_requirements(api_key, project_name, project_summary, requirements, number_requirements):
    """Use OpenAI API to generate new requirements based on provided data."""
    openai.api_key = api_key

    prompt = (f"Role: Act as a senior requirements analyst with expertise in requirements engineering and project management.\n"
              f"Situation: You are reviewing a project's requirement list with the following details:\n"
              f"Project Name: {project_name}; Project Summary: {project_summary}; Current Requirements: {requirements}.\n" 
              f"Task: Analyze the provided information, identify potential gaps in the current requirements, and generate {number_requirements} new relevant and not similar requirements that would be essential for the project's success in the following categories "
              f"(Functional requirements, Non-functional requirements, Integration requirements, Data requirements, User interface requirements, Compliance and regulatory requirements, Testing and validation requirements).\n"
              f"Structure your response following the format: [number] : [requirement] : [categorie]\n"
              f"Do not include introductory or concluding comments. Only provide the requirements in the specified format.")

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt}]
    )

    return response.choices[0].message.content

def save_new_requirements(new_requirements, output_file="new_generated_requirements.csv"):
    """Save generated requirements to a new CSV file."""
    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Requirement Number", "Requirement Description", "Requirement Category"])

        for line in new_requirements.strip().split("\n"):
            if line.strip():
                parts = line.split(":", 2)
                if len(parts) == 3:
                    writer.writerow(parts)

    return os.path.abspath(output_file)

def main():
    project_name, project_summary, csv_file_path, number_requirements = get_user_input()
    print(project_name +","+ project_summary +","+ csv_file_path +","+ number_requirements)

    try:
        requirements = upload_module(csv_file_path)
        print(requirements)
    except FileNotFoundError:
        print("Error: File not found. Please check the file path.")
        return

    api_key = input("Please enter your OpenAI API key: ")

    print("Generating new requirements based on the initial input...")
    new_requirements = generate_requirements(api_key, project_name, project_summary, requirements, number_requirements)

    output_file = save_new_requirements(new_requirements)

    print(f"New requirements have been saved to: {output_file}")

if __name__ == "__main__":
    main()
