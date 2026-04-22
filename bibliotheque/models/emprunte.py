# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Emprunte(models.Model):
    _name = 'bibliotheque.emprunte'
    _description = 'Emprunteurs'
    _rec_name = 'emprunteur_id'
    _inherit = 'mail.thread'

    emprunteur_id = fields.Many2one('res.partner', 'Emprunteur', domain="[('function', '!=', 'Etudiant')]")
    livre_id = fields.Many2one(comodel_name='bibliotheque.livre')
    image = fields.Binary(related='emprunteur_id.image_1920')
    etiquete = fields.Many2one(related='livre_id.etiquette_id')
    color = fields.Integer(related='etiquete.color', required=True)
    reference = fields.Char(related='livre_id.reference')
    date_emprunte = fields.Datetime('Date de prêt ', required=True, default=lambda self: fields.datetime.now())
    is_adhere = fields.Boolean('Retourné')
    date_retour = fields.Datetime('Date de retour', default=lambda self: fields.datetime.now())
    emprunteurs_ids = fields.One2many(related='livre_id.emprunteurs_ids')
    quantite_dispo = fields.Integer(related='livre_id.quantite_dispo')


    # récupérer les livres d'une etiquette particulier
    @api.model
    def onchange_etiquette_id(self):
        for fil in self:
            return {
                'domain': {'livre_id': [('etiquette_id', '=', fil.etiquete.id)]}}


