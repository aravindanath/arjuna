'''
This file is a part of Test Mile Arjuna
Copyright 2018 Test Mile Software Testing Pvt Ltd

Website: www.TestMile.com
Email: support [at] testmile.com
Creator: Rahul Verma

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

from .base import *
from .stage import TestStage
from arjuna.lib.unitee.engine.pool import TestObjectThreadPool
from arjuna.lib.unitee.types.containers import *
from arjuna.lib.unitee.enums import *
from arjuna.lib.unitee.state.states import *

class TestSession(TestObject):
	def __init__(self, defn):
		super().__init__(TestObjectTypeEnum.Session)
		self.defn = defn
		self.thcount = 1
		self.stages = []
		self.state = SessionState()
		self.fixture_defs = self.defn.fixture_defs
		self.append_before_fixture(self.fixture_defs.build(FixtureTypeEnum.INIT_SESSION))
		self.append_after_fixture(self.fixture_defs.build(FixtureTypeEnum.END_SESSION))

	def load(self, base_tvars=None):
		self._populate_tvars()
		for index, stage_def in enumerate(self.defn.stage_defs):
			stage = TestStage(index + 1, self, stage_def)
			stage.load(self.tvars.clone())
			self.stages.append(stage)
		self.children = self.stages

	def _populate_tvars(self):
		from arjuna.lib.core import ArjunaCore
		central_evars = ArjunaCore.config.clone_evars()
		self.tvars = TestVars()
		self.tvars.info.session = SessionInfo()
		self.tvars.info.session.meta['name'] = self.defn.name
		self.tvars.evars.update(ArjunaCore.config.clone_evars())
		self.tvars.evars.update(self.defn.evars)

	def _execute(self):
		tp = TestObjectThreadPool(self.thcount, self, "st")
		tp.run()