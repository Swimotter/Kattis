PROBLEM_DIR_FILE:=problemList.txt

.PHONY: clean

clean:
	while read dir; do \
		if [ -d "$$dir" ]; then \
			find "$$dir" -type f \( -name "*.o" -o -name "*.exe" \) -delete; \
		fi; \
	done < $(PROBLEM_DIR_FILE); \
