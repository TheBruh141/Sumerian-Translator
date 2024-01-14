cd ../photos

while true; do
    count=$(ls -l | grep "^-" | wc -l)
    echo "Number of files: $count"
    sleep 1
done