import sys
import json
import os
import argparse
from youtube_transcript_api import YouTubeTranscriptApi
import psutil
import time

def get_text_yt_transcript(video_id):
    """
    Retrieves the transcript of a YouTube video in English and German languages (if available).

    Args:
    video_id (str): The YouTube video ID for which to retrieve the transcript.

    Returns:
    str: The concatenated transcript text.
    """
    print(f"Attempting to retrieve the transcript for video ID: {video_id}...")
    try:
        # Attempt to retrieve the transcript of the video in English and German
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'en-US', 'de'])
        print("Transcript successfully retrieved.")
    except Exception as e:
        # If an exception is raised, print an error message and exit the program
        print("Error: Unable to retrieve YouTube transcript.")
        print(f"{e}")
        sys.exit(1)

    # Concatenate all of the text segments of the transcript together
    transcript_text = []
    for x in transcript:
        transcript_text.append(x["text"])

    # Join the list at the end
    transcript_text = " ".join(transcript_text)

    # Return the full transcript as a string
    return transcript_text

def save_transcript_as_txt(transcript_text, output_path):
    """
    Save the transcript text as a TXT file.

    Args:
    transcript_text (str): The transcript text to save.
    output_path (str): The path to the output TXT file.
    """
    with open(output_path, "w", encoding="utf-8") as txt_file:
        txt_file.write(transcript_text)
    print(f"Transcript saved as TXT at: {output_path}")

def save_transcript_as_json(transcript_text, output_path):
    """
    Save the transcript text as a JSON file.

    Args:
    transcript_text (str): The transcript text to save.
    output_path (str): The path to the output JSON file.
    """
    transcript_data = {"transcript": transcript_text}
    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(transcript_data, json_file, indent=4, ensure_ascii=False)
    print(f"Transcript saved as JSON at: {output_path}")

def main(video_id, to_text, to_json):
    start_time = time.time()
    process = psutil.Process(os.getpid())
    cpu_usage = process.cpu_percent(0.0)
    
    transcript_text = get_text_yt_transcript(video_id)
    
    # Define output file paths
    txt_output_path = f"{video_id}.txt"
    json_output_path = f"{video_id}.json"
    
    # Save the transcript in TXT and/or JSON formats based on the command-line arguments
    if to_text:
        save_transcript_as_txt(transcript_text, txt_output_path)
    
    if to_json:
        save_transcript_as_json(transcript_text, json_output_path)
    
    end_time = time.time()
    cpu_usage = process.cpu_percent(0.0)
    memory_info = process.memory_info()
    
    print(f"CPU usage: {cpu_usage}%")
    print(f"Memory usage: {memory_info.rss / (1024 * 1024):.2f} MB")
    print(f"Execution time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download and prepare YouTube transcripts for GPT models.")
    parser.add_argument("video_id", type=str, help="The YouTube video ID.")
    parser.add_argument("--to_text", action="store_true", help="Save transcript as TXT format.")
    parser.add_argument("--to_json", action="store_true", help="Save transcript as JSON format.")
    args = parser.parse_args()
    
    if not args.to_text and not args.to_json:
        print("Error: At least one of --to_text or --to_json must be specified.")
        sys.exit(1)
    
    main(args.video_id, args.to_text, args.to_json)