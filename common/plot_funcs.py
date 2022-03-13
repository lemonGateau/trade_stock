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


def plot_orders_hist(close, bids, asks):
    fig = plt.figure(figsize=(9.8, 4.6))

    plt.xlim(close.index[0], close.index[-1])
    plt.grid(True)

    plt.scatter(bids.index, bids, label="bid", marker="o", s=14, c="green")
    plt.scatter(asks.index, asks, label="ask", marker="s", s=14, c="red")
    plt.plot(close, label="close", c="blue", alpha=0.5)

    plt.legend()
    plt.show()
