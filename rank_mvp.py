"""
Michael Patel
May 2020

Project description:
    Use basketball reference data to rank every MVP winner's campaign since 2000

File description:
    Use basketball reference data to rank every MVP winner's campaign since 2000
"""
################################################################################


################################################################################
# Main
if __name__ == "__main__":
    mvp_df = mvp_df.sort_values(by=["HITP Index"], ascending=False)
