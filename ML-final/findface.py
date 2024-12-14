from deepface import DeepFace
 
# find returns list of pandas dataframes
while True:
    target = input("Write target file name: ")
    if target == "close":
        break
    dfs = DeepFace.find(img_path = "./targets/"+target, db_path = "images-2")
    merged_df = pd.DataFrame()  # Create an empty DataFrame to collect results
    # Perform face search using DeepFace
    # dfs = DeepFace.find(img_path=file_path, db_path=db_path)

    # Merge all DataFrames into one
    for df in dfs:
        merged_df = pd.concat([merged_df, df])

    # Clean up uploaded file
    # if os.path.exists(file_path):
        # os.remove(file_path)

# Extract unique student identities
    merged_df['student_id'] = merged_df['identity'].apply(lambda x: os.path.basename(os.path.dirname(x)))
    print(merged_df)
    unique_students = merged_df.drop_duplicates(subset="student_id")["student_id"].tolist()
    print(unique_students)


# # Reorganize the database by student ID
# reorganize_database(merged_df)
#     for df in dfs:
#         print(df.head())
