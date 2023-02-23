
class ChangeFile:

    def __init__(self, ref: str, keyword: str):
        self.file_ref = ref
        self.keyword = keyword

    def dochange(self):
        try:
            md_file = open(self.file_ref, "r", encoding="utf-8")
            lines = md_file.readlines()
            md_file.close()
            # Create a new list to store the modified lines
            new_lines = []
            in_code_block = False
            for line in lines:
                # Check if the line starts with ```
                if line.startswith("```"):
                    # Toggle the flag
                    in_code_block = not in_code_block

                    # If we are entering a code block, replace only the first occurrence of ``` with ```C++
                    if in_code_block:
                        new_line = line.replace(line.split(
                            "```")[1], self.keyword, 1)+'\n'
                    else:
                        # If we are exiting a code block, keep the line as it is
                        new_line = line

                else:
                    # If we are not inside a code block, keep the line as it is
                    new_line = line
                new_lines.append(new_line)

            # Open the same markdown file for writing
            md_file = open(self.file_ref, "w", encoding="utf-8")

            # Write all the new lines to the file
            md_file.writelines(new_lines)

            # Close the file
            md_file.close()
            return True
        except Exception as e:
            return e
