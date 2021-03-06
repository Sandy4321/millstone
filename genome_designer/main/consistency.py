"""Functions that enforce consistency.
"""


def ensure_variant_set_consistency(variant_set):
    """For all Variants in a VariantSet, makes an association to samples
    having GT_TYPE = 2.
    """
    for variant in variant_set.variants.all():
        vtvs = variant.varianttovariantset_set.get(variant_set=variant_set)
        for vccd in variant.variantcallercommondata_set.all():
            for ve in vccd.variantevidence_set.all():
                if 'GT_TYPE' in ve.data and ve.data['GT_TYPE'] == 2:
                    vtvs.sample_variant_set_association.add(
                            ve.experiment_sample)
                else:
                    vtvs.sample_variant_set_association.remove(
                            ve.experiment_sample)


def ensure_all_ref_genome_variant_set_consistency(reference_genome):
    """Ensures VariantSet consistency for all VariantSets belonging to a
    ReferenceGenome.
    """
    for vs in reference_genome.variantset_set.all():
        ensure_variant_set_consistency(vs)
    reference_genome.invalidate_materialized_view()
