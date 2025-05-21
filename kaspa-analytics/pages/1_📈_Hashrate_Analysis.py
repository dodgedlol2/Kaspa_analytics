# Update the figure creation section with these changes:

        # Enhanced layout with custom slider color
        fig.update_layout(
            template='plotly_dark',
            hovermode='x unified',
            height=700,
            margin=dict(l=20, r=20, t=60, b=100),
            yaxis_title='Hashrate (PH/s)',
            xaxis_title=x_title,
            xaxis=dict(
                rangeslider=dict(
                    visible=True,
                    thickness=0.1,
                    bgcolor='rgba(0, 0, 0, 0.3)',  # Darker, less distracting background
                    bordercolor="#2b3137",  # Matching the border color
                    borderwidth=1
                ),
                type="log" if x_scale_type == "Log" else None,
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(100,100,100,0.2)',
                minor=dict(
                    ticklen=6,
                    gridcolor='rgba(100,100,100,0.1)',
                    gridwidth=0.5
                ),
                tickformat=tickformat,
                range=[None, max_days] if x_scale_type == "Log" else 
                      [df['Date'].min(), genesis_date + pd.Timedelta(days=max_days)]
            ),
            yaxis=dict(
                type="log" if y_scale == "Log" else "linear",
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(100,100,100,0.2)',
                minor=dict(
                    ticklen=6,
                    gridcolor='rgba(100,100,100,0.1)',
                    gridwidth=0.5
                )
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

        # Group the power-law traces together
        power_law_traces = []
        
        # Main power-law fit trace (visible by default)
        power_law_trace = go.Scatter(
            x=fit_x,
            y=y_fit,
            mode='lines',
            name=f'Power-Law Fit (R²={r2:.3f})',
            line=dict(color='orange', dash='dot', width=1.5),
            visible=True
        )
        power_law_traces.append(power_law_trace)
        
        # Future projection line (dashed)
        future_proj_trace = go.Scatter(
            x=future_x,
            y=a * np.power(np.linspace(df['days_from_genesis'].max(), max_days, 30), b),
            mode='lines',
            name='Future Projection',
            line=dict(color='orange', dash='dot', width=1.5),
            visible=True,
            showlegend=False
        )
        power_law_traces.append(future_proj_trace)
        
        # Deviation bands (only shown when toggled)
        lower_band_trace = go.Scatter(
            x=fit_x,
            y=y_fit * 0.4,
            mode='lines',
            name='-60% Deviation',
            line=dict(color='rgba(150, 150, 150, 0.8)', dash='dot', width=1),
            hoverinfo='skip',
            visible=show_bands
        )
        power_law_traces.append(lower_band_trace)
        
        upper_band_trace = go.Scatter(
            x=fit_x,
            y=y_fit * 2.2,
            mode='lines',
            name='+120% Deviation',
            line=dict(color='rgba(150, 150, 150, 0.8)', dash='dot', width=1),
            hoverinfo='skip',
            visible=show_bands
        )
        power_law_traces.append(upper_band_trace)
        
        # Future bands
        future_lower_band_trace = go.Scatter(
            x=future_x,
            y=a * np.power(np.linspace(df['days_from_genesis'].max(), max_days, 30), b) * 0.4,
            mode='lines',
            line=dict(color='rgba(150, 150, 150, 0.8)', dash='dot', width=1),
            hoverinfo='skip',
            visible=show_bands,
            showlegend=False
        )
        power_law_traces.append(future_lower_band_trace)
        
        future_upper_band_trace = go.Scatter(
            x=future_x,
            y=a * np.power(np.linspace(df['days_from_genesis'].max(), max_days, 30), b) * 2.2,
            mode='lines',
            line=dict(color='rgba(150, 150, 150, 0.8)', dash='dot', width=1),
            hoverinfo='skip',
            visible=show_bands,
            showlegend=False
        )
        power_law_traces.append(future_upper_band_trace)
        
        # Add all traces to the figure
        fig.add_traces(power_law_traces)

        # Main trace (keep this separate)
        fig.add_trace(go.Scatter(
            x=x_values,
            y=df['Hashrate_PH'],
            mode='lines',
            name='Hashrate (PH/s)',
            line=dict(color='#00FFCC', width=2),
            hovertemplate='<b>Date</b>: %{text|%Y-%m-%d}<br><b>Hashrate</b>: %{y:.2f} PH/s<extra></extra>',
            text=df['Date']
        ))

        # Create a button to toggle all power-law related traces
        fig.update_layout(
            updatemenus=[
                dict(
                    type="buttons",
                    direction="right",
                    x=0.5,
                    y=1.15,
                    showactive=True,
                    buttons=list([
                        dict(
                            label="Show Power Law",
                            method="update",
                            args=[{"visible": [True] + [True]*len(power_law_traces)}]
                        ),
                        dict(
                            label="Hide Power Law",
                            method="update",
                            args=[{"visible": [True] + [False]*len(power_law_traces)}]
                        )
                    ])
                )
            ]
        )

        # Show the figure with more vertical space
        st.plotly_chart(fig, use_container_width=True)
