from random import sample, choice

from sqlalchemy import Column, Integer, Text, DateTime, func, Boolean
from sqlalchemy.orm import declarative_base

INSTRUMENTS = ['Drums', 'Bass', 'Guitar', 'Vocals', 'Synthesizer']

Base = declarative_base()


class BandMember(Base):
    __tablename__ = 'band member'
    id = Column(Integer, primary_key=True)
    present_next_rep = Column(Boolean(), default=False)
    instruments = Column(Text(length=1024))  # Инструменты через запятую
    name = Column(Text(length=65535))  # Имя
    created_at = Column(DateTime(), server_default=func.now())

    def __str__(self):
        return self.name


class Band:
    def __init__(self, members):
        self.members = members

    def instrument_present(self, instrument):
        for member in self.members:
            instruments = member.instruments.split(', ')
            if instrument in instruments:
                member.instruments = instrument
                return True
        return False

    def det_instrument(self):
        for member in self.members:
            instruments = member.instruments.split(', ')
            member.instruments = choice(instruments)

    def create_band(self, jam_members_count):
        sampled_band = Band([])
        while (not sampled_band.instrument_present('Bass')) or (not sampled_band.instrument_present('Drums')):
            sampled_band = Band(sample(self.members, k=jam_members_count))
        return sampled_band

    def __str__(self):
        names = [obj.name + ', ' for obj in self.members]
        names[-1] = names[-1].replace(',', '.')
        ret = "Band of " + "".join(names)
        return ret


if __name__ == '__main__':
    members = []
    members.append(BandMember(instruments='Guitar, Bass', name='Sanya'))
    members.append(BandMember(instruments='Drums', name='Andrew'))
    members.append(BandMember(instruments='Synthesizer', name='Nick'))
    members.append(BandMember(instruments='Guitar, Bass', name='Sanya'))
    members.append(BandMember(instruments='Guitar, Synthesizer', name='Eldar'))

    band = Band(members)
    new_band = band.create_band(3)
    print(new_band)
