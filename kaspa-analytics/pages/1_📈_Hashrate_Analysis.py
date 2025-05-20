# Updated figure configuration (replace your existing layout code)
fig.update_layout(
    template='plotly_dark',
    hovermode='x unified',
    height=700,
    title="Kaspa Hashrate Growth",
    yaxis_title='Hashrate (PH/s)',
    xaxis=dict(
        title='Days Since Genesis' if x_scale == "Log" else 'Date',
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(100,100,100,0.2)',
        showline=True,
        linewidth=2,
        linecolor='rgba(200,200,200,0.5)',
        mirror=True,  # Shows ticks on all sides
        ticks='inside',  # Puts ticks inside the graph
        ticklen=10,  # Base length
        tickwidth=2,  # Base width
        minor=dict(
            ticklen=6,
            tickwidth=1,
            tickcolor='rgba(200,200,200,0.7)',
            gridcolor='rgba(100,100,100,0.1)',
            gridwidth=0.5
        )
    ),
    yaxis=dict(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(100,100,100,0.2)',
        showline=True,
        linewidth=2,
        linecolor='rgba(200,200,200,0.5)',
        mirror=True,
        ticks='inside',
        ticklen=10,
        tickwidth=2,
        minor=dict(
            ticklen=6,
            tickwidth=1,
            tickcolor='rgba(200,200,200,0.7)',
            gridcolor='rgba(100,100,100,0.1)',
            gridwidth=0.5
        )
    )
)

# Enhanced log scale tick marks
if x_scale == "Log":
    fig.update_xaxes(
        type="log",
        tickmode='array',
        tickvals=np.concatenate([
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [10, 20, 30, 40, 50, 60, 70, 80, 90],
            [100, 200, 300, 400, 500, 600, 700, 800, 900]
        ]),
        ticktext=np.concatenate([
            ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
            ['10', '', '', '', '', '', '', '', ''],
            ['100', '', '', '', '', '', '', '', '']
        ]),
        ticklen=[8 if i%9==0 else 6 for i in range(27)],  # Longer at decades
        tickwidth=[2 if i%9==0 else 1.5 for i in range(27)],
        minor=dict(
            tickvals=np.concatenate([
                np.linspace(1, 10, 90),
                np.linspace(10, 100, 90),
                np.linspace(100, 1000, 90)
            ]),
            ticklen=4,
            tickwidth=1,
            tickcolor='rgba(200,200,200,0.5)'
        )
    )

if y_scale == "Log":
    fig.update_yaxes(
        type="log",
        tickmode='array',
        tickvals=[1, 10, 100, 1000],
        ticktext=['1', '10', '100', '1000'],
        ticklen=12,  # Longer at decades
        tickwidth=2.5,
        minor=dict(
            tickvals=np.concatenate([
                np.linspace(1, 10, 9),
                np.linspace(10, 100, 9),
                np.linspace(100, 1000, 9)
            ]),
            ticklen=6,
            tickwidth=1.5,
            tickcolor='rgba(200,200,200,0.5)'
        )
    )
