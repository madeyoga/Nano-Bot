package commands.awaiter;

public interface IResponseWaiter<T> {
    void register(T state);
    T getState(String identifier);
}
