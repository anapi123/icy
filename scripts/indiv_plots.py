import matplotlib.pyplot as plt
from create_big_df import concat_dfs


def main():
    dfs = concat_dfs()
    print(dfs)

if __name__ == "__main__":
    main()