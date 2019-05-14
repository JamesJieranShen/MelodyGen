## Model params based on data size

- 2 MB:
    - rnn_size 256 (or 128)
    - layers 2
    - seq_length 64
    - batch_size 32
    - dropout 0.25
- 5-8 MB:
    - rnn_size 512
    - layers 2 (or 3)
    - seq_length 128
    - batch_size 64
    - dropout 0.25