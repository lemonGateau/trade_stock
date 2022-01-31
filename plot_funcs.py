import matplotlib.pyplot as plt


def plot_df_sub(dfs):
    fig = plt.figure(figsize=(8, 13))

    for i in range(len(dfs)):
        plt.subplot(len(dfs), 1, i+1)

        plt.xlim(dfs[i].index[0], dfs[i].index[-1])
        plt.plot(dfs[i])
        plt.grid(True)
        # plt.tight_layout()

    plt.show()
