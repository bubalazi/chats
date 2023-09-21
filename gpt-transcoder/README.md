# `gpt-transcoder` - Video Transcoding Script with GPT-4 Assistance

## Overview

This wiki page documents the development of a Bash script for video transcoding. The script was developed with the assistance of GPT-4, and it aims to transcode existing videos to optimize them for video streaming.

## Requirements

The script needed to fulfill the following requirements:

1. Check if NVIDIA hardware-accelerated FFMPEG exists and use it; otherwise, fallback to CPU.
2. Support multiple video file extensions.
3. Aim for lossless compression.
4. Include logging at critical steps.
5. Include a dry-run operation argument.
6. Generate a tabulated report with aligned columns and descriptive headers.

## Iterations

### Iteration 1: Initial Script

The initial script was divided into two separate files: `transcode_dir.sh` and `check_file.sh`. The first script was responsible for finding video files in a directory, while the second script handled the transcoding and renaming tasks.

### Iteration 2: Combining Scripts and Adding Features

The two scripts were combined into a single file, and additional features were added to meet the requirements. This included argument parsing, logging, and a dry-run option.

### Iteration 3: Debugging and Refinement

Several issues were identified and fixed, including:

- Incorrect sequence of logging messages.
- Timer not incrementing in the final report.

## Final Script

The final script is a comprehensive solution that meets all the requirements. It includes robust error handling, logging, and reporting features.

\`\`\`bash
# (Insert the final script here)
\`\`\`

## Usage

To use the script, run the following command:

\`\`\`bash
./script.sh -t /path/to/target -r -n
\`\`\`

## Conclusion

The development process involved multiple iterations and debugging steps. The final script is a robust and flexible solution for video transcoding, optimized for both CPU and NVIDIA hardware acceleration.