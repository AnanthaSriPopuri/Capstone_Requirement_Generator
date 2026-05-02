SHELL_STORIES = [
    {
        "id":"SH-01","type":"Analysis","priority":"Must Have",
        "story":"As a data analyst at the organisation, I want a shell script that reads any entity CSV and prints a status frequency table with counts and percentages so that I get a quick operational summary without loading data into memory.",
        "acceptance":["Accepts filename as $1","Excludes header row","Shows value, count, and percentage","Sorted by frequency descending","Prints total record count"],
        "script":"""#!/bin/bash
# SH-01: Status Frequency Table
FILE=$1
[ -z "$FILE" ] && echo "Usage: $0 <csvfile>" && exit 1
TOTAL=$(tail -n +2 "$FILE" | wc -l)
echo "=== Status Frequency: $FILE (Total: $TOTAL) ==="
tail -n +2 "$FILE" | awk -F',' '{print $NF}' | sed 's/^ *//;s/ *$//' | sort | uniq -c | sort -rn | awk -v tot="$TOTAL" '{pct=($1/tot)*100; printf "%-22s %-8d %.2f%%\\n", $2, $1, pct}'"""
    },
    {
        "id":"SH-02","type":"Analysis","priority":"Must Have",
        "story":"As a finance controller at the organisation, I want a shell script that computes sum, average, min, and max of any numeric column so that I can generate financial summaries from the command line.",
        "acceptance":["Accepts filename and column number","Skips non-numeric rows","Output formatted to 2 decimals","Shows count of processed rows"],
        "script":"""#!/bin/bash
# SH-02: Numeric Column Statistics
FILE=$1; COL=${2:-4}
[ -z "$FILE" ] && echo "Usage: $0 <csvfile> <col_number>" && exit 1
tail -n +2 "$FILE" | awk -F',' -v c="$COL" '$c ~ /^-?[0-9]+(\\.?[0-9]*)?$/ {v=$c+0; sum+=v; count++; if(NR==1||v<mn)mn=v; if(NR==1||v>mx)mx=v} END {printf "Count:%d Sum:%.2f Avg:%.2f Min:%.2f Max:%.2f\\n",count,sum,sum/count,mn,mx}'"""
    },
    {
        "id":"SH-03","type":"Analysis","priority":"Must Have",
        "story":"As a BI lead at the organisation, I want a shell script that extracts the top N records by a numeric column and saves them as a dated CSV report so that decision-makers can review high-priority entries.",
        "acceptance":["Accepts filename, column, N","Preserves header","Saves to topN_report_YYYYMMDD.csv","Reports rows written"],
        "script":"""#!/bin/bash
# SH-03: Top N Records
FILE=$1; COL=${2:-4}; N=${3:-10}
OUT="top${N}_report_$(date +%Y%m%d).csv"
head -1 "$FILE" > "$OUT"
tail -n +2 "$FILE" | sort -t',' -k"$COL" -rn | head -"$N" >> "$OUT"
echo "Top $N by col $COL -> $OUT ($(tail -n +2 $OUT | wc -l) rows)" """
    },
    {
        "id":"SH-04","type":"Analysis","priority":"Must Have",
        "story":"As an operations manager at the organisation, I want a shell script to group entity records by month from a date column so that I can spot seasonal trends.",
        "acceptance":["Accepts filename and date column","Shows YYYY-MM format","Sorted chronologically"],
        "script":"""#!/bin/bash
# SH-04: Monthly Distribution
FILE=$1; DCOL=${2:-6}
echo "Monthly Distribution: $FILE"
tail -n +2 "$FILE" | awk -F',' -v d="$DCOL" '{v=$d; if(match(v,/^[0-9]{4}-[0-9]{2}/)) print substr(v,1,7)}' | sort | uniq -c | awk '{printf "%-12s %d\\n",$2,$1}'"""
    },
    {
        "id":"SH-05","type":"Analysis","priority":"Must Have",
        "story":"As a data quality lead at the organisation, I want a shell script that audits every column for null/empty values and saves a DQ scorecard CSV so that remediation priorities are clear.",
        "acceptance":["Auto-detects all columns","Reports null count and percentage","Flags columns above 5% null rate","Saves to dq_scorecard_YYYYMMDD.csv"],
        "script":"""#!/bin/bash
# SH-05: Data Quality Audit
FILE=$1
TOTAL=$(tail -n +2 "$FILE" | wc -l)
OUT="dq_scorecard_$(date +%Y%m%d).csv"
echo "ColNum,FieldName,NullCount,NullPct,Status" > "$OUT"
COLS=$(head -1 "$FILE" | tr ',' '\\n' | wc -l)
HEADS=$(head -1 "$FILE")
for i in $(seq 1 $COLS); do
  FNAME=$(echo "$HEADS" | cut -d',' -f"$i" | tr -d '\\r')
  CNT=$(tail -n +2 "$FILE" | cut -d',' -f"$i" | grep -Ec '^[[:space:]]*$|^NULL$|^N/A')
  PCT=$(awk "BEGIN{printf \\"%.1f\\",($CNT/$TOTAL)*100}")
  ST="OK"; [ $(awk "BEGIN{print($PCT>5)?1:0}") -eq 1 ] && ST="ALERT"
  echo "$i,$FNAME,$CNT,$PCT%,$ST" >> "$OUT"
done
echo "Saved: $OUT"; cat "$OUT" """
    },
    {
        "id":"SH-06","type":"Analysis","priority":"Should Have",
        "story":"As a system auditor at the organisation, I want a shell script that compares two versions of an entity file and reports added, removed, and common record counts so that daily data load changes are tracked automatically.",
        "acceptance":["Accepts two filenames","Reports added, removed, common counts","Ignores header in comparison"],
        "script":"""#!/bin/bash
# SH-06: File Diff Summary
OLD=$1; NEW=$2
echo "Old: $(tail -n +2 $OLD | wc -l)  New: $(tail -n +2 $NEW | wc -l)"
echo "Added: $(comm -13 <(tail -n +2 $OLD|sort) <(tail -n +2 $NEW|sort) | wc -l)"
echo "Removed: $(comm -23 <(tail -n +2 $OLD|sort) <(tail -n +2 $NEW|sort) | wc -l)"
echo "Common: $(comm -12 <(tail -n +2 $OLD|sort) <(tail -n +2 $NEW|sort) | wc -l)" """
    },
    {
        "id":"SH-07","type":"Analysis","priority":"Should Have",
        "story":"As a data science lead at the organisation, I want a shell script that detects outliers (values > 3x the column average) in any numeric field so that anomalies can be flagged for investigation.",
        "acceptance":["Accepts filename and column number","Computes average and 3x threshold","Lists outlier row numbers and values"],
        "script":"""#!/bin/bash
# SH-07: Outlier Detection
FILE=$1; COL=${2:-4}
AVG=$(tail -n +2 "$FILE" | awk -F',' -v c=$COL '$c~/^-?[0-9.]+$/{s+=$c;n++}END{if(n>0)print s/n}')
THRESH=$(awk "BEGIN{print $AVG*3}")
echo "Avg=$AVG Threshold=$THRESH"
tail -n +2 "$FILE" | awk -F',' -v c=$COL -v t=$THRESH '$c+0>t+0{print NR": "$c}' | head -20"""
    },
    {
        "id":"SH-08","type":"Analysis","priority":"Should Have",
        "story":"As a reporting manager at the organisation, I want a shell script to generate a frequency distribution CSV for any categorical column so it can be attached to weekly stakeholder emails.",
        "acceptance":["Accepts filename and column number","Output is valid CSV","Sorted by frequency descending","Saved as freq_dist_YYYYMMDD.csv"],
        "script":"""#!/bin/bash
# SH-08: Frequency Distribution CSV
FILE=$1; COL=${2:-5}
OUT="freq_dist_col${COL}_$(date +%Y%m%d).csv"
TOTAL=$(tail -n +2 "$FILE" | wc -l)
echo "Value,Frequency,Percentage" > "$OUT"
tail -n +2 "$FILE" | cut -d',' -f"$COL" | sed 's/^ *//;s/ *$//' | sort | uniq -c | sort -rn | awk -v tot=$TOTAL '{pct=($1/tot)*100; printf "%s,%d,%.2f%%\\n",$2,$1,pct}' >> "$OUT"
echo "Saved: $OUT"; cat "$OUT" """
    },
    {
        "id":"SH-09","type":"Cleaning","priority":"Must Have",
        "story":"As a data remediation engineer at the organisation, I want a shell script that removes all exact duplicate rows from any entity CSV (keeping first occurrence) and saves the deduplicated output so that downstream processes receive unique records.",
        "acceptance":["Preserves header row","Removes exact duplicates","Saves to entity_deduped_YYYYMMDD.csv","Reports rows removed"],
        "script":"""#!/bin/bash
# SH-09: Deduplicate CSV
FILE=$1
[ -z "$FILE" ] && echo "Usage: $0 <csvfile>" && exit 1
BASE=$(basename "$FILE" .csv)
OUT="${BASE}_deduped_$(date +%Y%m%d).csv"
ORIG=$(tail -n +2 "$FILE" | wc -l)
head -1 "$FILE" > "$OUT"
tail -n +2 "$FILE" | sort -u >> "$OUT"
CLEAN=$(tail -n +2 "$OUT" | wc -l)
echo "Input:$ORIG  Output:$CLEAN  Removed:$((ORIG-CLEAN))  File:$OUT" """
    },
    {
        "id":"SH-10","type":"Cleaning","priority":"Must Have",
        "story":"As a data pipeline engineer at the organisation, I want a shell script that trims whitespace, replaces empty/NULL fields with UNKNOWN, removes corrupt ID rows, and deduplicates — saving a fully clean file — so that the data passes all validation checks before database loading.",
        "acceptance":["All 4 stages run in sequence","Empty and NULL replaced with UNKNOWN","Corrupt ID rows removed","Duplicate rows removed","Audit trail printed after each stage"],
        "script":"""#!/bin/bash
# SH-10: Full Cleaning Pipeline
FILE=$1
[ -z "$FILE" ] && echo "Usage: $0 <csvfile>" && exit 1
BASE=$(basename "$FILE" .csv)
OUT="${BASE}_cleaned_$(date +%Y%m%d).csv"
T1=/tmp/${BASE}_s1.csv; T2=/tmp/${BASE}_s2.csv; T3=/tmp/${BASE}_s3.csv
echo "=== Cleaning Pipeline: $FILE ==="
sed 's/ *, */,/g; s/^[[:space:]]*//; s/[[:space:]]*$//' "$FILE" > "$T1"
echo "[S1] Whitespace trim: $(tail -n +2 $T1 | wc -l) rows"
awk -F',' 'BEGIN{OFS=","}{for(i=1;i<=NF;i++){gsub(/^[[:space:]]+|[[:space:]]+$/,"",$i);if($i==""||$i=="NULL"||$i=="N/A")$i="UNKNOWN"}print}' "$T1" > "$T2"
echo "[S2] Null fix: $(tail -n +2 $T2 | wc -l) rows"
head -1 "$T2" > "$T3"
tail -n +2 "$T2" | grep -v '^\\?\\?' | grep -v '^,' >> "$T3"
echo "[S3] Corrupt IDs removed: $(tail -n +2 $T3 | wc -l) rows"
head -1 "$T3" > "$OUT"
tail -n +2 "$T3" | sort -u >> "$OUT"
echo "[S4] Dedup done: $(tail -n +2 $OUT | wc -l) rows"
echo "Final file: $OUT"
rm -f "$T1" "$T2" "$T3" """
    },
]

def generate_shell_stories(entity_config, sector_data):
    return SHELL_STORIES