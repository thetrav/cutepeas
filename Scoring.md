# Notes #

A simple implementation I thought of is as follows:
The pea maintain a list of bounces on its way down (the pea is a bounce listener notified by the Physics engine)
When the pea is finished bouncing, the Scoring engine is notified, and takes the list, and calculates a score.

This has potential to make a neat animation where you can list score per bounce in the peas speech bubble, or in a side bar, or even use particles to make them fly out of the pea, and then collapse into one single super score, with multipliers being applied in between.