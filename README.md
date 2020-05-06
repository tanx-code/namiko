# namiko

这个项目更偏向于 proof of concept，它不会关心实际运行效率，在 Python 上关注这个没有意义，我只关心它在模型架构上的效率，因此不要在生产中使用。

整个项目采用迭代式开发，

1，先写一个只能处理一个 client 的 http server。
2，再写一个多线程版本的 http server，看看最多 1s 可以处理多少个 client，以及判断出处理能力与线程数量的关系。
3，再使用 epoll，看看最多 1s 可以处理多少个 client。

上述过程会通过 commit history 来进行记录。
