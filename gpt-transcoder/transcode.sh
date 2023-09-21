#!/bin/bash

# Global variables
total_real_time=0
total_duration=0
declare -A EXTENSION_COUNTS
readonly SUPPORTED_EXTENSIONS=("mkv" "avi" "flv")
readonly NVIDIA_CODEC="hevc_nvenc"
readonly CPU_CODEC="libx264"
recursive_flag=""
dry_run=0
target_location=""

# Argument parser
usage() {
  echo "Usage: $0 [options]"
  echo "Options:"
  echo "  -t, --target     Target location to operate on"
  echo "  -r, --recursive  Enable recursive search"
  echo "  -n, --dry-run    Enable dry-run mode"
  exit 1
}

while (( "$#" )); do
  case "$1" in
    -t|--target)
      target_location="$2"
      shift 2
      ;;
    -r|--recursive)
      recursive_flag="-r"
      shift
      ;;
    -n|--dry-run)
      dry_run=1
      shift
      ;;
    -*|--*=)
      echo "Error: Unsupported flag $1"
      usage
      ;;
    *)
      usage
      ;;
  esac
done

if [ -z "$target_location" ]; then
  echo "Error: Target location must be specified."
  usage
fi

# Check for NVIDIA hardware acceleration
if ffmpeg -hide_banner -encoders | grep -q "$NVIDIA_CODEC"; then
  CODEC="$NVIDIA_CODEC"
  HWACCEL_FLAGS="-hwaccel cuda -hwaccel_output_format cuda"
else
  CODEC="$CPU_CODEC"
  HWACCEL_FLAGS=""
fi

transcode() {
  local video="$1"
  local preset=""

  if [ "$CODEC" == "$NVIDIA_CODEC" ]; then
    preset="slow"
  else
    preset="veryslow"
  fi

  echo "[LOG] Converting: $video"

  if [ "$dry_run" -eq 0 ]; then
    local real_time=$( { time ffmpeg -v warning -y $HWACCEL_FLAGS \
      -i "$video" \
      -c:v $CODEC -preset $preset \
      -movflags +faststart \
      -c:a copy "$video.mp4"; } 2>&1 )
  
    local real_seconds=$(echo "$real_time" | awk '/real/ {split($2, a, "m"); print a[1]*60 + a[2]}')
    
    if [ -n "$real_seconds" ]; then
      total_real_time=$(echo "$total_real_time + $real_seconds" | bc)
    fi
  fi
}

rename_file() {
  local video="$1"

  if [ "$dry_run" -eq 0 ]; then
    mv "$video" "$video.backup"
  fi
  echo "[LOG] Renamed: $video to $video.backup"
}

# Main function
main() {
  local total_files=0
  local find_depth=""
  
  if [ -z "$recursive_flag" ]; then
    find_depth="-maxdepth 1"
  fi

  for ext in "${SUPPORTED_EXTENSIONS[@]}"; do
    while read -r file; do
      EXTENSION_COUNTS[$ext]=$((EXTENSION_COUNTS[$ext] + 1))
      transcode "$file"
      rename_file "$file"
      total_files=$((total_files + 1))
    done < <(find "$target_location" $find_depth -type f -name "*.${ext}")
  done

  # Generate report
  printf "%-15s %s\n" "Extension" "Count"
  for ext in "${!EXTENSION_COUNTS[@]}"; do
    printf "%-15s %d\n" "$ext" "${EXTENSION_COUNTS[$ext]}"
  done

  printf "%-15s %.3f\n" "Total Time:" "$total_real_time"

  if [ -n "$total_files" ] && [ "$total_files" -gt 0 ]; then
    avg_time=$(echo "scale=2; $total_real_time / $total_files" | bc)
    printf "%-15s %.2f\n" "Average Time:" "$avg_time"
  fi
}


# Entry point
main
