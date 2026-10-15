"""Toy model with a hard-coded constant (the patch-knob test artifact)."""
lengthscale = 0.01


def model(alpha):
    return {"score": 100.0 * alpha * (1 + 10 * lengthscale), "aux": 50.0 * (1 + 20 * lengthscale)}
