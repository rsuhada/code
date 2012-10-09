from numpy import *

a = random.random((20, 22))

def distance(array, xpos, ypos):
    # probably a gazillion methods to create the actual distances...
    # if you array is large and you are only interested to a certain size
    # you sould probably slice out a smaller one first of course.
    dists = sqrt(arange(-xpos, array.shape[0]-xpos, dtype=float)[:,None]**2
          + arange(-ypos, array.shape[1]-ypos, dtype=float)[None,:]**2)
    return dists

# Prepare which bins to use:
dists = distance(a, 10, 11).astype(int)

# Do a bincount with weights.
result = bincount(dists.flat, weights=a.flat)
# and add them up:
result = add.accumulate(result)

# print a
# print distance
# print result

xcen_obj = 1.0
ycen_obj = 1.0
im_conv = arange(1, 10, 1, dtype='double').reshape(3,3)

# new approach
# dists = distance(im_conv, xcen_obj, ycen_obj).astype(int)
dists = distance(im_conv, xcen_obj, ycen_obj).astype(int)
result_geom = bincount(dists.flat)
result = bincount(dists.flat, weights=im_conv.flat)
# result = add.accumulate(result)

# standard
(r, profile_ref, geometric_area) = extract_profile_generic(im_conv, xcen_obj, ycen_obj)

print im_conv
print dists

print 20*"#"
print r
print profile_ref

print 20*"#"
print result, result_geom

# result = bincount(dists.flat, weights=a.flat)




