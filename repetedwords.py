#!/usr/bin/env python3
"""
Word Counter Script
Counts the number of occurrences of each word in a text file.
"""

import re
import sys
from collections import Counter
from pathlib import Path


def clean_word(word):
    """
    Clean a word by removing punctuation and converting to lowercase.
    
    Args:
        word (str): The word to clean
        
    Returns:
        str: Cleaned word or empty string if word is invalid
    """
    # Remove punctuation and convert to lowercase
    cleaned = re.sub(r'[^\w\s]', '', word.lower().strip())
    return cleaned if cleaned else None


def count_words_from_file(file_path, case_sensitive=False, ignore_common_words=False):
    """
    Count occurrences of each word in a text file.
    
    Args:
        file_path (str): Path to the text file
        case_sensitive (bool): Whether to treat words as case sensitive
        ignore_common_words (bool): Whether to ignore common words like 'the', 'and', etc.
        
    Returns:
        Counter: Counter object with word counts
    """
    # Common words to ignore (if requested)
    common_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
        'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
        'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must',
        'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
        'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their'
    }
    
    word_counts = Counter()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                # Split line into words
                words = line.split()
                
                for word in words:
                    if case_sensitive:
                        cleaned_word = word.strip()
                    else:
                        cleaned_word = clean_word(word)
                    
                    # Skip empty words
                    if not cleaned_word:
                        continue
                    
                    # Skip common words if requested
                    if ignore_common_words and cleaned_word.lower() in common_words:
                        continue
                    
                    word_counts[cleaned_word] += 1
                    
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except PermissionError:
        print(f"Error: Permission denied to read file '{file_path}'.")
        return None
    except UnicodeDecodeError:
        print(f"Error: Unable to decode file '{file_path}'. Try a different encoding.")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None
    
    return word_counts


def display_results(word_counts, top_n=None, min_count=1):
    """
    Display word count results in a formatted way.
    
    Args:
        word_counts (Counter): Counter object with word counts
        top_n (int): Show only top N most frequent words
        min_count (int): Show only words with at least this many occurrences
    """
    if not word_counts:
        print("No words found or error occurred.")
        return
    
    # Filter by minimum count
    filtered_counts = {word: count for word, count in word_counts.items() if count >= min_count}
    
    if not filtered_counts:
        print(f"No words found with at least {min_count} occurrence(s).")
        return
    
    # Sort by count (descending) and then by word (ascending)
    sorted_words = sorted(filtered_counts.items(), key=lambda x: (-x[1], x[0]))
    
    # Limit to top N if specified
    if top_n:
        sorted_words = sorted_words[:top_n]
    
    print(f"\nWord Count Results (showing {len(sorted_words)} words):")
    print("-" * 50)
    print(f"{'Word':<20} {'Count':<10}")
    print("-" * 50)
    
    for word, count in sorted_words:
        print(f"{word:<20} {count:<10}")
    
    print("-" * 50)
    print(f"Total unique words: {len(word_counts)}")
    print(f"Total word occurrences: {sum(word_counts.values())}")


def main():
    """Main function to run the word counter."""
    if len(sys.argv) < 2:
        print("Usage: python repetedwords.py <text_file> [options]")
        print("\nOptions:")
        print("  --case-sensitive    Treat words as case sensitive")
        print("  --ignore-common     Ignore common words (the, and, etc.)")
        print("  --top <number>      Show only top N most frequent words")
        print("  --min-count <number> Show only words with at least N occurrences")
        print("\nExample: python repetedwords.py sample.txt --top 10 --ignore-common")
        return
    
    file_path = sys.argv[1]
    
    # Parse command line options
    case_sensitive = '--case-sensitive' in sys.argv
    ignore_common = '--ignore-common' in sys.argv
    
    # Get top N parameter
    top_n = None
    if '--top' in sys.argv:
        try:
            top_index = sys.argv.index('--top')
            if top_index + 1 < len(sys.argv):
                top_n = int(sys.argv[top_index + 1])
        except (ValueError, IndexError):
            print("Error: Invalid --top parameter. Must be a number.")
            return
    
    # Get min count parameter
    min_count = 1
    if '--min-count' in sys.argv:
        try:
            min_index = sys.argv.index('--min-count')
            if min_index + 1 < len(sys.argv):
                min_count = int(sys.argv[min_index + 1])
        except (ValueError, IndexError):
            print("Error: Invalid --min-count parameter. Must be a number.")
            return
    
    print(f"Analyzing file: {file_path}")
    print(f"Case sensitive: {case_sensitive}")
    print(f"Ignore common words: {ignore_common}")
    
    # Count words
    word_counts = count_words_from_file(file_path, case_sensitive, ignore_common)
    
    if word_counts is not None:
        display_results(word_counts, top_n, min_count)
    else:
        print("Failed to process the file.")


if __name__ == "__main__":
    main()
