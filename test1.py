from numpy import random

edu6_choices = ['<12 grade', 'HS graduate', 'post hs/no college', 'associate degree/some college',
                'bachelors degree', 'graduate school']
edu6_distribution = [1, 2, 3, 4, 5, 4]
edu6_rand_sum = sum(edu6_distribution)
for i in range(0, len(edu6_distribution)):
    edu6_distribution[i] /= edu6_rand_sum

edu6_draw = edu6_choices.index(random.choice(edu6_choices, 1, p=edu6_distribution)) \
            + 1  # education index must increase by 1 when pass to Person class

done = [False] * len(edu6_choices)

print('Person    {}'.format(edu6_choices[edu6_draw]))
