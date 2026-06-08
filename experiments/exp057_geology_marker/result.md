# exp057: Geology Marker TVT Prediction

**Pooled CV RMSE: 1217.7498**

## Comparison
- exp022 (Particle Filter): 11.024
- exp014 (Geometry): 13.53
- exp057 (Geology Marker): 1217.7498

## Broken Wells
- Rescued: 0 / 47

## Method
- Classify each well by GR mean similarity to typewell geology
- Use mean TVT of matched geology as prediction
- leak-free fold separation
