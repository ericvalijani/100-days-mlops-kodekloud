#!/bin/sh

set -euo pipefail

# Update README.md progress and day solution link.

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
root_dir=$(CDPATH= cd -- "$script_dir/.." && pwd)
readme_file="$root_dir/README.md"

target_input=${1:-}
if [[ -n "$target_input" ]]; then
	if [[ "$target_input" = /* ]]; then
		target_file="$target_input"
	else
		target_file="$root_dir/$target_input"
	fi
else
	new_file=$(CDPATH= cd -- "$root_dir/days" && ls | tail -n 1)
	target_file="$root_dir/days/$new_file"
fi

if [[ -z "$target_file" || ! -f "$target_file" ]]; then
	printf 'No day file found to publish.\n' >&2
	exit 1
fi

case "$target_file" in
	"$root_dir"/*) rel_target=${target_file#"$root_dir/"} ;;
	*) rel_target=$target_file ;;
esac

day_number=$(printf '%s' "$rel_target" | sed -n 's#.*day\([0-9][0-9]*\)/.*#\1#p')
if [[ -z "$day_number" ]]; then
	day_number=$(printf '%s' "$(basename -- "$target_file")" | sed -n 's/[^0-9]*\([0-9][0-9]*\).*/\1/p')
fi

if [[ -z "$day_number" ]]; then
	printf 'Cannot infer day number from %s\n' "$target_file" >&2
	exit 1
fi

day_index=$((10#$day_number))
day_label=$(printf '%02d' "$day_index")

solution_link="[Solved]($rel_target)"

total_days=100
tmp_table=$(mktemp)
tmp_file=$(mktemp)
trap 'rm -f "$tmp_table" "$tmp_file"' EXIT

awk -v day="$day_label" -v solution="$solution_link" '
function trim(value) {
	sub(/^[[:space:]]+/, "", value)
	sub(/[[:space:]]+$/, "", value)
	return value
}

function rebuild_row(line,   parts, count) {
	count = split(line, parts, "|")
	if (count < 6) {
		return line
	}

	parts[5] = " " solution " "
	return parts[1] "|" parts[2] "|" parts[3] "|" parts[4] "|" parts[5] "|" parts[6]
}

{
	if ($0 ~ "^\\| " day " \\|") {
		print rebuild_row($0)
		next
	}

	print
}
' "$readme_file" > "$tmp_table"

completed_days=$(find "$root_dir/days" -type f -name '*.md' | wc -l | tr -d '[:space:]')

progress_percent=0
if [[ "$total_days" -gt 0 ]]; then
	progress_percent=$((completed_days * 100 / total_days))
fi

awk -v progress="$progress_percent" '
{
	if ($0 ~ /progress-bar\.xyz/) {
		print "![" progress "%](https://progress-bar.xyz/" progress ")"
		next
	}

	print
}
' "$tmp_table" > "$tmp_file"

mv "$tmp_file" "$readme_file"
trap - EXIT

printf 'Updated %s with day %s and %s%% progress.\n' "$readme_file" "$day_label" "$progress_percent"
