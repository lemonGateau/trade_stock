import matplotlib.pyplot as plt


def plot_df(df_list):
    fig = plt.figure(figsize=(9.8, 4.6))

    
    for i in range(len(df_list)):
        plt.subplot(len(df_list), 1, i+1)

        plt.xlim(df_list[i].index[0], df_list[i].index[-1])
        plt.grid(True)
        plt.plot(df_list[i])

    # plt.tight_layout()
    plt.show()

